import asyncio
from datetime import datetime
import json
import os
import yarl
import logging
import aiohttp

import azure.functions as func
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
                await asyncio.sleep(float(resp.headers.get("X-RateLimit-Reset") or 5) - datetime.utcnow().timestamp())
                continue

            elif resp.status == 200:
                return await resp.json()
            else:
                raise RuntimeError(f"Unknown status code {resp.status}: {await resp.json()}")



async def main(event: func.EventGridEvent):
    body: SlashCommand = event.get_json()
    logging.info(str(body))
    data: SlashData = body["data"]
    options: ListOptionsData = cast(ListOptionsData, data.get('options'))
    opts: Dict[str, OptionsData] = {}

    for x in options:
        opts[x['name']] = x
    
    option1 = opts['option1']['value']

    async with aiohttp.ClientSession() as session:
        await make_request(session, f"webhooks/{os.environ['DiscordApplicationID']}/{body['token']}", "POST", {
            "content": f"Sent from Event Grid consumer, option1 is {option1}",
            "allowed_mentions": { "parse": [] }
            })
    
