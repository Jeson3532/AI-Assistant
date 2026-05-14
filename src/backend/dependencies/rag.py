from fastapi import Request, Depends

from langchain_qdrant.qdrant import QdrantVectorStore
from langchain_ollama import ChatOllama
from langgraph.graph.state import CompiledStateGraph

def get_vectorstore(request: Request) -> QdrantVectorStore:
    return request.app.state.qdrant_vectorstore


def get_prompts(request: Request) -> dict:
    return request.app.state.prompts


def load_llm(request: Request) -> ChatOllama:
    return request.app.state.llm


def get_llm_graph(request: Request) -> CompiledStateGraph:
    return request.app.state.llm_graph
