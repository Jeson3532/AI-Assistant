# src/tests/test_assistant.py

import pytest
import json
from unittest.mock import MagicMock, AsyncMock
from langchain_core.messages.ai import AIMessage

from src.backend.dependencies.rag import get_llm_graph

QUERY_PAYLOAD = {
    "query": "Как оформить заявку?",
    "history": [],
}

QUERY_PAYLOAD_WITH_HISTORY = {
    "query": "Расскажи подробнее",
    "history": [
        {"role": "user", "text": "Привет"},
        {"role": "assistant", "text": "Здравствуйте! Чем могу помочь?"},
    ],
}


def make_ai_message(content: str = "Вот инструкция по оформлению заявки.") -> AIMessage:
    msg = MagicMock(spec=AIMessage)
    msg.id = "msg-test-id-001"
    msg.content = content
    return msg


def make_graph_result(
        content: str = "Вот инструкция по оформлению заявки.",
        dialog_type: str = "consultation",
        operator: bool = False,
) -> dict:
    return {
        "response": make_ai_message(content),
        "dialog_type": dialog_type,
        "operator": operator,
    }


@pytest.mark.asyncio
async def test_send_query_success(client, app, auth_headers):
    mock_graph = AsyncMock()
    mock_graph.ainvoke = AsyncMock(return_value=make_graph_result())
    app.dependency_overrides[get_llm_graph] = lambda: mock_graph

    resp = await client.post("/assistant/", json=QUERY_PAYLOAD, headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == "msg-test-id-001"
    assert data["query"] == QUERY_PAYLOAD["query"]
    assert data["dialog_type"] == "consultation"
    assert data["operator"] is False
    assert data["model_response"] == "Вот инструкция по оформлению заявки."


@pytest.mark.asyncio
async def test_send_query_with_history(client, app, auth_headers):
    mock_graph = AsyncMock()
    mock_graph.ainvoke = AsyncMock(return_value=make_graph_result(content="Подробнее: шаг 1, шаг 2."))
    app.dependency_overrides[get_llm_graph] = lambda: mock_graph

    resp = await client.post("/assistant/", json=QUERY_PAYLOAD_WITH_HISTORY, headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["model_response"] == "Подробнее: шаг 1, шаг 2."

    call_kwargs = mock_graph.ainvoke.call_args.args[0]
    assert len(call_kwargs["history"]) == 2
    assert call_kwargs["history"][0]["role"] == "user"


@pytest.mark.asyncio
async def test_send_query_operator_escalation(client, app, auth_headers):
    mock_graph = AsyncMock()
    mock_graph.ainvoke = AsyncMock(return_value=make_graph_result(
        content="Передаю вас менеджеру.",
        dialog_type="complaint",
        operator=True,
    ))
    app.dependency_overrides[get_llm_graph] = lambda: mock_graph

    resp = await client.post("/assistant/", json=QUERY_PAYLOAD, headers=auth_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["operator"] is True
    assert data["dialog_type"] == "complaint"


@pytest.mark.asyncio
async def test_send_query_missing_query_field(client, auth_headers):
    resp = await client.post("/assistant/", json={"history": []}, headers=auth_headers)
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_send_query_unauthorized(client_no_auth):
    resp = await client_no_auth.post("/assistant/", json={"query": "test", "history": []})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_send_query_empty_query_string(client, app, auth_headers):
    mock_graph = AsyncMock()
    mock_graph.ainvoke = AsyncMock(return_value=make_graph_result(content="Уточните запрос."))
    app.dependency_overrides[get_llm_graph] = lambda: mock_graph

    resp = await client.post("/assistant/", json={"query": "", "history": []}, headers=auth_headers)

    assert resp.status_code == 200


async def make_sse_stream(events: list[dict]):
    for event in events:
        yield f"data: {json.dumps(event)}\n\n".encode()
    yield b"data: [DONE]\n\n"


def build_mock_graph_stream(events: list[dict]):
    async def _astream_events(payload, version):
        for event in events:
            yield event

    mock_graph = MagicMock()
    mock_graph.astream_events = _astream_events
    return mock_graph


@pytest.mark.asyncio
async def test_stream_query_success(client, app, auth_headers):
    ai_response = make_ai_message("Стриминговый ответ ассистента.")

    stream_events = [
        {"event": "on_chain_start", "name": "classification_dialog_type", "data": {}},
        {"event": "on_chain_end", "name": "classification_dialog_type",
         "data": {"output": {"dialog_type": "consultation"}}},
        {"event": "on_chain_start", "name": "search", "data": {}},
        {"event": "on_chain_end", "name": "reranker", "data": {"output": {"rerank_scores": [0.91, 0.75]}}},
        {
            "event": "on_chain_end",
            "name": "response",
            "data": {"output": {"response": ai_response, "operator": False}},
        },
    ]

    mock_graph = build_mock_graph_stream(stream_events)
    app.dependency_overrides[get_llm_graph] = lambda: mock_graph

    resp = await client.post("/assistant/stream/", json=QUERY_PAYLOAD, headers=auth_headers)

    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers["content-type"]

    raw = resp.text
    assert "[DONE]" in raw

    result_event = None
    for line in raw.splitlines():
        if line.startswith("data:") and "[DONE]" not in line:
            payload = json.loads(line.removeprefix("data:").strip())
            if payload.get("type") == "result":
                result_event = payload
                break

    assert result_event is not None
    assert result_event["model_response"] == "Стриминговый ответ ассистента."
    assert result_event["dialog_type"] == "consultation"
    assert result_event["operator"] is False
    assert result_event["score"] == 0.91


@pytest.mark.asyncio
async def test_stream_query_emits_status_events(client, app, auth_headers):
    stream_events = [
        {"event": "on_chain_start", "name": "classification_dialog_type", "data": {}},
        {"event": "on_chain_start", "name": "search", "data": {}},
        {"event": "on_chain_start", "name": "reranker", "data": {}},
    ]

    mock_graph = build_mock_graph_stream(stream_events)
    app.dependency_overrides[get_llm_graph] = lambda: mock_graph

    resp = await client.post("/assistant/stream/", json=QUERY_PAYLOAD, headers=auth_headers)

    assert resp.status_code == 200
    status_events = []
    for line in resp.text.splitlines():
        if line.startswith("data:") and "[DONE]" not in line:
            payload = json.loads(line.removeprefix("data:").strip())
            if payload.get("type") == "status":
                status_events.append(payload)

    assert len(status_events) == 3


@pytest.mark.asyncio
async def test_stream_query_operator_escalation(client, app, auth_headers):
    ai_response = make_ai_message("Передаю менеджеру.")

    stream_events = [
        {"event": "on_chain_end", "name": "classification_dialog_type",
         "data": {"output": {"dialog_type": "complaint"}}},
        {
            "event": "on_chain_end",
            "name": "call_operator",
            "data": {"output": {"response": ai_response, "operator": True}},
        },
    ]

    mock_graph = build_mock_graph_stream(stream_events)
    app.dependency_overrides[get_llm_graph] = lambda: mock_graph

    resp = await client.post("/assistant/stream/", json=QUERY_PAYLOAD, headers=auth_headers)

    assert resp.status_code == 200
    result_event = None
    for line in resp.text.splitlines():
        if line.startswith("data:") and "[DONE]" not in line:
            payload = json.loads(line.removeprefix("data:").strip())
            if payload.get("type") == "result":
                result_event = payload
                break

    assert result_event is not None
    assert result_event["operator"] is True
    assert result_event["dialog_type"] == "complaint"


@pytest.mark.asyncio
async def test_stream_query_unauthorized(client_no_auth):
    resp = await client_no_auth.post("/assistant/stream/", json={"query": "test", "history": []})
    assert resp.status_code == 401
