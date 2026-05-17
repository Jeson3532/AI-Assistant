from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from src.backend.schemas.assistant.input import SendQueryModel
from src.backend.schemas.assistant.response import AssistantResponse
from src.backend.dependencies.rag import get_llm_graph
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages.ai import AIMessage
import json

router = APIRouter(prefix='/assistant', tags=['Assistant', 'Ассистент'])

NODE_STATUS_MAP = {
    "classification_dialog_type": "🔍 Определяем тип обращения...",
    "search": "📚 Ищем ответ в базе знаний...",
    "reranker": "⚙️ Готовим результаты...",
    "response": "✍️ Формируем ответ...",
    "clarify": "🤔 Уточняем детали...",
    "call_operator": "👨‍💼 Передаём менеджеру...",
    "small_talk": "💬 Отвечаем...",
}

FINAL_NODES = {"response", "clarify", "call_operator", "small_talk"}


@router.post("/", response_model=AssistantResponse)
async def send_query(
        body: SendQueryModel,
        llm: CompiledStateGraph = Depends(get_llm_graph)):
    result = await llm.ainvoke({
        "query": body.query,
        "history": [m.model_dump() for m in body.history]
    })
    response = result['response']
    return AssistantResponse(
        id=response.id,
        query=body.query,
        dialog_type=result.get("dialog_type"),
        operator=result.get("operator", False),
        model_response=response.content,
    )


@router.post("/stream/")
async def stream_query(
        body: SendQueryModel,
        llm: CompiledStateGraph = Depends(get_llm_graph)):
    async def event_generator():
        accumulated = {"dialog_type": None}

        async for event in llm.astream_events(
                {"query": body.query, "history": [m.model_dump() for m in body.history]},
                version="v2"
        ):
            kind = event.get("event")
            name = event.get("name", "")

            if kind == "on_chain_start" and name in NODE_STATUS_MAP:
                yield f"data: {json.dumps({'type': 'status', 'text': NODE_STATUS_MAP[name]})}\n\n"

            elif kind == "on_chain_end" and name == "classification_dialog_type":
                output = event.get("data", {}).get("output", {})
                accumulated["dialog_type"] = output.get("dialog_type")

            elif kind == "on_chain_end" and name in FINAL_NODES:
                output = event.get("data", {}).get("output", {})
                response = output.get("response")
                operator = output.get("operator", False)

                if response:
                    yield f"data: {json.dumps(
                        {'type': 'result', 
                         'model_response': response.content, 
                         'operator': operator, 
                         'dialog_type': accumulated['dialog_type']})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
