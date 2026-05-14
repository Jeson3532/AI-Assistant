from src.services.rag.states.base import BasicState
from src.services.rag.methods.type_classification import get_dialog_type
from src.services.rag.search.service import hybrid_search
from src.services.rag.search.reranker import rerank_docs
from src.services.rag.service import generate_response
from langchain_core.language_models import BaseChatModel
from langchain_qdrant import QdrantVectorStore
from src.services.rag.tools import operator
from src.services.rag.utils.prompts import load_prompts
from langchain_core.prompts import ChatPromptTemplate

__all__ = ["classify_node", "hybrid_search_node", "rerank_docs_node", "generate_response_node"]
PROMPTS = load_prompts()


async def classify_node(state: BasicState, llm: BaseChatModel):
    dialog_type = await get_dialog_type(llm, state['query'])
    return {"dialog_type": dialog_type}


async def hybrid_search_node(state: BasicState, vector_store: QdrantVectorStore):
    docs = await hybrid_search(vector_store, state['query'], state['dialog_type'])
    return {"docs": docs}


def rerank_docs_node(state: BasicState, reranker, tokenizer):
    docs = state['docs']

    if not docs:
        return {
            "reranked_docs": [],
            "rerank_scores": []
        }

    reranked_docs, scores = rerank_docs(reranker, tokenizer, state['query'], docs)
    return {
        "reranked_docs": reranked_docs,
        "rerank_scores": scores
    }


async def generate_response_node(state: BasicState, llm: BaseChatModel):
    response = await generate_response(
        llm,
        state['query'],
        state['reranked_docs'],
        state['dialog_type']
    )
    return {"response": response}


async def clarify_node(state: BasicState, llm: BaseChatModel):
    prompt = PROMPTS.get("clarify")
    template = ChatPromptTemplate.from_template(prompt)
    chain = template | llm
    response = await chain.ainvoke({"query": state['query']})
    return {"response": response}


async def call_operator_node(state: BasicState, llm: BaseChatModel):
    prompt = PROMPTS.get("call_operator")
    template = ChatPromptTemplate.from_template(prompt)
    chain = template | llm
    response = await chain.ainvoke({
        "query": state['query']
    })

    # передача оператору
    # call_result = operator.call_operator(
    #     user_query=state['query'],
    #     dialog_type=state['dialog_type'],
    #     response=response.get("content", None))

    return {"response": response}
