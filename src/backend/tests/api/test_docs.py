# src/tests/test_docs.py

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.backend.dependencies.rag import get_vectorstore, get_async_client

UPLOAD_PAYLOAD = {
    "title": "Тестовый документ",
    "content": "Содержимое тестового документа для загрузки в базу знаний.",
    "type": "consultation",
    "chunk_size": 500,
}

COLLECTION_DATA = [
    {
        "id": "abc-123",
        "payload": {
            "metadata": {"title": "Тестовый документ", "dialog_type": "consultation"},
            "page_content": "Содержимое тестового документа.",
        },
    }
]


@pytest.mark.asyncio
async def test_upload_docs_success(client, auth_headers):
    with patch("src.backend.routes.docs.load_dict_document") as mock_load:
        mock_load.return_value = None

        resp = await client.post("/docs/", json=UPLOAD_PAYLOAD, headers=auth_headers)

    assert resp.status_code == 200
    assert resp.json() == {"success": True}
    mock_load.assert_called_once()


@pytest.mark.asyncio
async def test_upload_docs_calls_loader_with_correct_chunk_size(client, auth_headers):
    with patch("src.backend.routes.docs.load_dict_document") as mock_load:
        mock_load.return_value = None

        payload = {**UPLOAD_PAYLOAD, "chunk_size": 300}
        await client.post("/docs/", json=payload, headers=auth_headers)

    _, kwargs = mock_load.call_args if mock_load.call_args.kwargs else (mock_load.call_args.args, {})
    call_args = mock_load.call_args
    assert call_args is not None
    assert call_args.kwargs.get("chunk_size") == 300 or call_args.args[2] == 300


@pytest.mark.asyncio
async def test_upload_docs_unauthorized(client_no_auth):
    resp = await client_no_auth.post("/docs/", json={
        "title": "Test", "content": "Content", "type": "consultation", "chunk_size": 500
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_upload_docs_missing_required_fields(client, auth_headers):
    with patch("src.backend.routes.docs.load_dict_document"):
        resp = await client.post("/docs/", json={"title": "Только заголовок"}, headers=auth_headers)

    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_get_docs_success(client, app, auth_headers):
    mock_qdrant = AsyncMock()

    with patch("src.backend.routes.docs.get_collection_data", new=AsyncMock(return_value=COLLECTION_DATA)) as mock_get:
        app.dependency_overrides[get_async_client] = lambda: mock_qdrant

        resp = await client.get("/docs/", params={"collection_name": "test_collection"}, headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_docs_unauthorized(client_no_auth):
    resp = await client_no_auth.get("/docs/", params={"collection_name": "test"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_docs_missing_collection_name(client, auth_headers):
    with patch("src.backend.routes.docs.get_collection_data", new=AsyncMock(return_value=[])):
        resp = await client.get("/docs/", headers=auth_headers)

    assert resp.status_code == 422
