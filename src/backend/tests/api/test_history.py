# src/backend/tests/api/test_history.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from src.backend.dependencies.services import get_db_service


def make_dialog_orm():
    obj = MagicMock()
    obj.id = 1
    obj.user_id = 42
    obj.username = "test_user"
    obj.dialog_type = "consultation"
    obj.operator = False
    obj.score = 0.95
    obj.history = [{"role": "user", "text": "Привет"}]
    obj.finished_at = datetime(2024, 1, 1, 12, 0, 0)
    return obj


def make_db_mock(app, **method_overrides):
    mock_history_repo = AsyncMock()
    for method, return_value in method_overrides.items():
        getattr(mock_history_repo, method).return_value = return_value

    mock_db = AsyncMock()
    mock_db.history = mock_history_repo
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    app.dependency_overrides[get_db_service] = lambda: mock_db
    return mock_db


SAVE_PAYLOAD = {
    "user_id": 42,
    "username": "test_user",
    "dialog_type": "consultation",
    "operator": False,
    "score": 0.95,
    "history": [{"role": "user", "text": "Привет"}],
}

ANALYTICS_DATA = {
    "total": 100,
    "auto_handled": 80,
    "operator_handled": 20,
    "score": 0.87,
    "by_type": [
        {"dialog_type": "consultation", "count": 60},
        {"dialog_type": "complaint", "count": 40},
    ],
}


@pytest.mark.asyncio
async def test_save_dialog(client, app, auth_headers):
    saved = make_dialog_orm()
    make_db_mock(app, save_dialog=saved)

    resp = await client.post("/history/", json=SAVE_PAYLOAD, headers=auth_headers)

    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_get_dialogs(client, app, auth_headers):
    items = [make_dialog_orm()]
    make_db_mock(app, get_all_dialogs=items)

    resp = await client.get("/history/", headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["user_id"] == 42
    assert data[0]["dialog_type"] == "consultation"


@pytest.mark.asyncio
async def test_get_dialogs_returns_empty_list(client, app, auth_headers):
    make_db_mock(app, get_all_dialogs=[])

    resp = await client.get("/history/", headers=auth_headers)

    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_history_unauthorized(client_no_auth):
    resp = await client_no_auth.get("/history/")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_analytics(client, app, auth_headers):
    make_db_mock(app, get_analytics=ANALYTICS_DATA)

    resp = await client.get("/analytics/", headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 100
    assert data["auto_handled"] == 80
    assert data["operator_handled"] == 20
    assert data["score"] == 0.87
    assert len(data["by_type"]) == 2


@pytest.mark.asyncio
async def test_get_analytics_unauthorized(client_no_auth):
    resp = await client_no_auth.get("/analytics/")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_journal_no_filters(client, app, auth_headers):
    items = [make_dialog_orm()]
    make_db_mock(app, get_dialogs_filtered=(items, 1))

    resp = await client.get("/analytics/journal/", headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["limit"] == 20
    assert data["offset"] == 0


@pytest.mark.asyncio
async def test_get_journal_with_filters(client, app, auth_headers):
    make_db_mock(app, get_dialogs_filtered=([], 0))

    resp = await client.get(
        "/analytics/journal/",
        params={"user_id": 42, "dialog_type": "consultation", "operator": False, "limit": 5, "offset": 10},
        headers=auth_headers,
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_get_journal_unauthorized(client_no_auth):
    resp = await client_no_auth.get("/analytics/journal/")
    assert resp.status_code == 401
