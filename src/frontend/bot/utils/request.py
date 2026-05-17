import aiohttp as ahttp
import os
from typing import AsyncGenerator
import json

BACKEND_URL = os.getenv("BACKEND_URL")
BACKEND_SECRET = os.getenv("SECRET")


async def send_assistant_query(query: str,
                               history: list[dict],
                               endpoint: str = '/assistant/'):
    try:
        async with ahttp.ClientSession(base_url=BACKEND_URL) as session:
            async with session.post(endpoint, headers={"x-secret-key": BACKEND_SECRET}, json={
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
        async with session.post("/assistant/stream/", headers={"x-secret-key": BACKEND_SECRET}, json={
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


async def save_dialog(
        user_id: int,
        username: str | None,
        dialog_type: str | None,
        operator: bool,
        history: list[dict],
):
    async with ahttp.ClientSession(base_url=BACKEND_URL) as session:
        await session.post("/history/", headers={"x-secret-key": BACKEND_SECRET}, json={
            "user_id": user_id,
            "username": username,
            "dialog_type": dialog_type,
            "operator": operator,
            "history": history,
        })


async def get_analytics() -> dict:
    async with ahttp.ClientSession(base_url=BACKEND_URL) as session:
        async with session.get("/analytics/", headers={"x-secret-key": BACKEND_SECRET}) as response:
            if response.status != 200:
                raise RuntimeError(f"Ошибка {response.status}: {await response.text()}")
            return await response.json()


async def get_journal(
        limit: int = 5,
        offset: int = 0,
        operator: bool | None = None,
        dialog_type: str | None = None,
) -> dict:
    params = {"limit": limit, "offset": offset}
    if operator is not None:
        params["operator"] = str(operator).lower()
    if dialog_type:
        params["dialog_type"] = dialog_type

    async with ahttp.ClientSession(base_url=BACKEND_URL) as session:
        async with session.get("/analytics/journal/", params=params,
                               headers={"x-secret-key": BACKEND_SECRET}) as response:
            if response.status != 200:
                raise RuntimeError(f"Ошибка {response.status}: {await response.text()}")
            return await response.json()
