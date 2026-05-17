import aiohttp as ahttp
import os
from typing import AsyncGenerator
import json

BACKEND_URL = os.getenv("BACKEND_URL")


async def send_assistant_query(query: str,
                               history: list[dict],
                               endpoint: str = '/assistant/'):
    try:
        async with ahttp.ClientSession(base_url=BACKEND_URL) as session:
            async with session.post(endpoint, json={
                "query": query,
                "history": history or []
            }) as response:
                if response.status != 200:
                    raise RuntimeError(f"Ошибка {response.status}: {await response.text()}")
                return await response.json()
    except Exception:
        raise


async def stream_assistant_query(
        query: str,
        history: list[dict]
) -> AsyncGenerator[dict, None]:
    async with ahttp.ClientSession(base_url=BACKEND_URL) as session:
        async with session.post("/assistant/stream/", json={
            "query": query,
            "history": history or []
        }) as response:
            if response.status != 200:
                raise RuntimeError(f"Ошибка {response.status}: {await response.text()}")

            async for line in response.content:
                line = line.decode("utf-8").strip()
                if line.startswith("data:"):
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    yield json.loads(data)
