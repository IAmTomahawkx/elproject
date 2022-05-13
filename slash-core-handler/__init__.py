import asyncio
from datetime import datetime
import json
import os
import yarl
import logging
import aiohttp

import azure.functions as func
from typing import Literal, Dict, Any, Optional
from .types import SlashCommand

base = yarl.URL("https://discord.com/api/v10/")

class Unauthorized(Exception):
    pass

async def make_request(session: aiohttp.ClientSession, route: str, method: Literal["GET", "PUT", "POST", "PATCH", "DELETE"], body: Optional[Dict[str, Any]]=None) -> Optional[dict]:
    while True:
        async with session.request(method, base / route, json=body, headers={"Authorization": f"Bot {os.environ['DiscordBotToken']}"}) as resp:
            if resp.status == 204:
                return None
            
            elif resp.status == 401:
                raise Unauthorized()
            
            elif resp.status == 429:
                await asyncio.sleep(float(resp.headers["X-Ratelimit-Reset"]) - datetime.utcnow().timestamp())
                continue

            elif resp.status == 200:
                return await resp.json()



async def main(event: func.EventGridEvent):
    data: SlashCommand = event.get_json()

    async with aiohttp.ClientSession() as session:
        await make_request(session, f"webhooks/{os.environ['DiscordApplicationID']}/{data['token']}", "POST", {"content": "Umbra Sucks"})
    
