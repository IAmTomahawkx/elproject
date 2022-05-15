import logging

import azure.functions as func

import yarl
import aiohttp
import asyncio
import json
import os
import datetime
from typing import Literal, Dict, Any, Optional, cast
from .types import *

base = yarl.URL("https://discord.com/api/v10/")

class Unauthorized(Exception):
    pass

async def make_request(session: aiohttp.ClientSession, route: str, method: Literal["GET", "PUT", "POST", "PATCH", "DELETE"], body: Optional[Dict[str, Any]]=None) -> Optional[dict]:
    for attempt in range(5):
        async with session.request(method, base / route, json=body, headers={"Authorization": f"Bot {os.environ['DiscordBotToken']}", "Content-Type": "application/json"}) as resp:
            if resp.status == 204:
                return None
            
            elif resp.status == 401:
                raise Unauthorized()
            
            elif resp.status == 429:
                logging.warning("Sleeping due to 429, bucket %s, reset %s, headers %s", resp.headers.get("X-RateLimit-Bucket"), resp.headers.get("X-RateLimit-Reset"), dict(resp.headers))
                await asyncio.sleep(float(resp.headers.get("X-RateLimit-Reset") or 5) - datetime.datetime.utcnow().timestamp())
                continue

            elif resp.status == 200:
                return await resp.json()
            else:
                raise RuntimeError(f"Unknown status code {resp.status}: {await resp.json()}")

async def main(msg: func.ServiceBusMessage):
    logging.info('Python ServiceBus queue trigger processed message: %s',
                 msg.get_body().decode('utf-8'))

    data = msg.get_body().decode("utf-8")
    body: SlashCommand = json.loads(data)

    options: ListOptionsData = cast(ListOptionsData, body.get('options'))
    opts: Dict[str, OptionsData] = {}

    for x in options:
        opts[x['name']] = x
    
    option1 = opts['option1']['value']

    async with aiohttp.ClientSession() as session:
        await make_request(session, f"webhooks/{os.environ['DiscordApplicationID']}/{body['token']}", "POST", {
            "content": f"Sent from queue consumer, option1 is {option1}",
            "allowed_mentions": { "parse": [] }
            })
    

