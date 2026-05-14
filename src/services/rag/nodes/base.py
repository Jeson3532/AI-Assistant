from src.services.rag.states.base import BasicState
from src.services.rag.methods.type_classification import get_dialog_type
from src.services.rag.search.service import hybrid_search
from src.services.rag.search.reranker import rerank_docs
from src.services.rag.service import generate_response
from langchain_core.language_models import BaseChatModel
from langchain_qdrant import QdrantVectorStore

__all__ = ["classify_node", "hybrid_search_node", "rerank_docs_node", "generate_response_node"]


def classify_node(state: BasicState, llm: BaseChatModel):
    dialog_type = get_dialog_type(llm, state['query'])
    return {"dialog_type": dialog_type}


def hybrid_search_node(state: BasicState, vector_store: QdrantVectorStore):
    docs = hybrid_search(vector_store, state['query'], state['dialog_type'])
    return {"docs": docs}


def rerank_docs_node(state: BasicState):
    reranked_docs, scores = rerank_docs(state['query'], state['docs'])
    return {
        "reranked_docs": reranked_docs,
        "rerank_scores": scores
    }


def generate_response_node(state: BasicState, llm: BaseChatModel):
    response = generate_response(
        llm,
        state['query'],
        state['reranked_docs'],
        state['dialog_type']
    )
    return {"response": response}
