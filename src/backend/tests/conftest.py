# src/backend/tests/conftest.py

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from src.backend.routes import routers
from src.backend.dependencies.auth import auth_user
from src.backend.dependencies.rag import get_llm_graph, get_vectorstore, get_async_client
from src.backend.dependencies.services import get_db_service


def build_app(override_auth: bool = True) -> FastAPI:
    application = FastAPI()
    for router in routers:
        application.include_router(router)

    if override_auth:
        application.dependency_overrides[auth_user] = lambda: "test-user"

    application.dependency_overrides[get_llm_graph] = lambda: AsyncMock()
    application.dependency_overrides[get_vectorstore] = lambda: MagicMock()
    application.dependency_overrides[get_async_client] = lambda: AsyncMock()
    application.dependency_overrides[get_db_service] = lambda: AsyncMock()

    return application


@pytest.fixture(scope="session")
def app():
    return build_app(override_auth=True)


@pytest.fixture(scope="session")
def app_no_auth():
    return build_app(override_auth=False)


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def client_no_auth(app_no_auth):
    async with AsyncClient(transport=ASGITransport(app=app_no_auth), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def auth_headers():
    return {"x-secret-key": "test-secret"}