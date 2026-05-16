from src.backend.services.rag.states.base import BasicState
from src.backend.services.rag.methods.type_classification import get_dialog_type
from src.backend.services.rag.search.service import hybrid_search
from src.backend.services.rag.search.reranker import rerank_docs
from src.backend.services.rag.service import generate_response
from langchain_core.language_models import BaseChatModel
from langchain_qdrant import QdrantVectorStore
from src.backend.services.rag.utils.prompts import load_prompts
from langchain_core.prompts import ChatPromptTemplate
import asyncio
from src.backend.utils.log import logger

__all__ = ["classify_node", "hybrid_search_node", "rerank_docs_node", "generate_response_node"]
PROMPTS = load_prompts()


async def classify_node(state: BasicState, llm: BaseChatModel):
    logger.info("Классификация диалога")
    dialog_type = await get_dialog_type(llm, state['query'])
    logger.info(f"Тип диалога: {dialog_type}")
    return {"dialog_type": dialog_type}


async def hybrid_search_node(state: BasicState, vector_store: QdrantVectorStore):
    logger.info("Гибридный поиск")
    docs = await hybrid_search(vector_store, state['query'], state['dialog_type'])
    return {"docs": docs}


async def rerank_docs_node(state: BasicState, reranker, tokenizer):
    logger.info("Реранкер")
    docs = state['docs']

    if not docs:
        return {"reranked_docs": [], "rerank_scores": []}

    loop = asyncio.get_event_loop()
    reranked_docs, scores = await loop.run_in_executor(
        None,
        rerank_docs, reranker, tokenizer, state['query'], docs
    )
    return {
        "reranked_docs": reranked_docs,
        "rerank_scores": scores
    }


async def generate_response_node(state: BasicState, llm: BaseChatModel):
    logger.info("Генерация ответа")
    history = state.get("history") or []
    logger.info(f"История диалога: {history}")
    response = await generate_response(
        llm,
        state['query'],
        state.get("reranked_docs", []),
        state['dialog_type'],
        history
    )
    return {"response": response}


async def clarify_node(state: BasicState, llm: BaseChatModel):
    logger.info("Уточняющий вопрос")
    response = await generate_response(
        model=llm,
        user_query=state['query'],
        docs=state.get("reranked_docs", []),
        dialog_type=state['dialog_type'],
        history=state.get("history") or [],
    )
    return {"response": response}


async def call_operator_node(state: BasicState, llm: BaseChatModel):
    logger.info("Вызов оператора")
    response = await generate_response(
        model=llm,
        user_query=state['query'],
        docs=state.get("reranked_docs", []),
        dialog_type=state['dialog_type'],
        history=state.get("history") or [],
    )

    return {"response": response, "operator": True}


