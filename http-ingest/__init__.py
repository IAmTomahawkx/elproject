from datetime import datetime
import os
import logging
import json
import uuid
import aiohttp

import azure.functions as func
from azure.core.credentials import AzureKeyCredential
import azure.eventgrid as eventgrid
from azure.eventgrid.aio import EventGridPublisherClient

from nacl.signing import VerifyKey

default_response_payload = json.dumps({"type": 5})

class InteractionType:
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4

def verify_key(raw_body: bytes, signature: str, timestamp: str, client_public_key: str) -> bool:
    message = timestamp.encode() + raw_body
    try:
        vk = VerifyKey(bytes.fromhex(client_public_key))
        vk.verify(message, bytes.fromhex(signature))
        return True
    except Exception as ex:
        logging.error("Error while verifying payload", exc_info=ex)
    
    return False

async def main(request: func.HttpRequest) -> func.HttpResponse:
    public_key = os.environ["DiscordPublicKey"]
    signature = request.headers.get('X-Signature-Ed25519')
    timestamp = request.headers.get('X-Signature-Timestamp')
    body = request.get_body()
    if signature is None or timestamp is None or not verify_key(body, signature, timestamp, public_key):
        return func.HttpResponse('Bad request signature', status_code=401)
    
    data = json.loads(body)
    if data["type"] == InteractionType.PING:
        return func.HttpResponse(json.dumps({
            "type": 1
        }))

    producer = EventGridPublisherClient(os.environ["EventGridConnectionURL"], AzureKeyCredential(os.environ["EventGridConnectionKey"]))

    async with producer:
        payload = {
            "subject": "/slashcommand",
            "id": str(uuid.uuid4()),
            "topic": os.environ["EventGridTopic"],
            "eventType": "slashcommand.created",
            "eventTime": datetime.utcnow().isoformat(),
            "data": data,
            "dataVersion": "1",
            "metadataVersion": "1"
        }
        await producer.send(payload)

    return func.HttpResponse(default_response_payload, headers={"Content-Type": "application/json"})
