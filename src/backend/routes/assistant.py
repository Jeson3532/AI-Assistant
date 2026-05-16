from fastapi import APIRouter, Depends
from src.backend.schemas.assistant.input import SendQueryModel
from src.backend.schemas.assistant.response import AssistantResponse
from src.backend.dependencies.rag import get_llm_graph
from langgraph.graph.state import CompiledStateGraph

router = APIRouter(prefix='/assistant', tags=['Assistant', 'Ассистент'])


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
