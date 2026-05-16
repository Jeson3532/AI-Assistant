from fastapi import APIRouter, Depends
from src.backend.schemas.assistant.input import SendQueryModel
from src.backend.dependencies.rag import get_llm_graph
from langgraph.graph.state import CompiledStateGraph

router = APIRouter(prefix='/assistant', tags=['Assistant', 'Ассистент'])


@router.post("/")
async def send_query(
        body: SendQueryModel,
        llm: CompiledStateGraph = Depends(get_llm_graph)):
    result = await llm.ainvoke({"query": body.query})
    response = result['response']
    return {
        "id": response.id,
        "query": body.query,
        "dialog_type": result.get("dialog_type", None),
        "model_response": response.content,
    }
