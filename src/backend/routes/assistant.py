from fastapi import APIRouter, Depends
from langchain_qdrant.qdrant import QdrantVectorStore
from src.schemas.assistant.input import SendQueryModel
from src.backend.dependencies.rag import get_llm_graph
from src.services.rag.graphs.build import build_graph
from src.services.rag.states.base import BasicState
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from langgraph.graph.state import CompiledStateGraph

router = APIRouter(prefix='/assistant', tags=['Assistant', 'Ассистент'])


@router.post("/")
async def send_query(
        body: SendQueryModel,
        llm: CompiledStateGraph = Depends(get_llm_graph)):
    response = await llm.ainvoke({"query": body.query})
    return response
