from langgraph.graph import StateGraph, START, END
from functools import partial
from typing import TypedDict, Type
from langchain_core.language_models import BaseChatModel
from langchain_qdrant import QdrantVectorStore
from src.services.rag.nodes.conditional import confidence_router

from src.services.rag.nodes import base as base_nodes


def build_graph(
        state: type[TypedDict],
        llm: BaseChatModel,
        vector_store: QdrantVectorStore):
    graph = StateGraph(state)

    graph.add_node("classification_dialog_type", partial(base_nodes.classify_node, llm=llm))
    graph.add_node("search", partial(base_nodes.hybrid_search_node, vector_store=vector_store))
    graph.add_node("reranker", base_nodes.rerank_docs_node)
    graph.add_node("response", partial(base_nodes.generate_response_node, llm=llm))
    graph.add_node("clarify", partial(base_nodes.clarify_node, llm=llm))
    graph.add_node("call_operator", partial(base_nodes.call_operator_node, llm=llm))

    graph.add_edge(START, "classification_dialog_type")
    graph.add_edge("classification_dialog_type", "search")
    graph.add_edge("search", "reranker")

    graph.add_conditional_edges(
        "reranker",
        confidence_router,
        {"response": "response",
         "clarify": "clarify",
         "call_operator": "call_operator"}
    )
    graph.add_edge("reranker", "response")

    # end edges
    graph.add_edge("clarify", END)
    graph.add_edge("response", END)
    graph.add_edge("call_operator", END)


    return graph.compile()
