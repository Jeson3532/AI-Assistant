from fastapi import Request, Depends

from langchain_qdrant.qdrant import QdrantVectorStore
from langchain_ollama import ChatOllama
from langgraph.graph.state import CompiledStateGraph
from qdrant_client import AsyncQdrantClient


def get_vectorstore(request: Request) -> QdrantVectorStore:
    return request.app.state.qdrant_vectorstore


def get_async_client(request: Request) -> AsyncQdrantClient:
    return request.app.state.qdrant_async_client


def get_prompts(request: Request) -> dict:
    return request.app.state.prompts


def load_llm(request: Request) -> ChatOllama:
    return request.app.state.llm


def get_llm_graph(request: Request) -> CompiledStateGraph:
    return request.app.state.llm_graph
