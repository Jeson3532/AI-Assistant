from langgraph.graph import StateGraph, START, END
from functools import partial
from typing import TypedDict, Type
from langchain_core.language_models import BaseChatModel
from langchain_qdrant import QdrantVectorStore
from src.services.rag.nodes.conditional import confidence_router, dialog_type_router

from src.services.rag.nodes import base as base_nodes


def build_graph(
        reranker,
        tokenizer,
        state: type[TypedDict],
        llm: BaseChatModel,
        classifier_llm: BaseChatModel,
        vector_store: QdrantVectorStore):
    graph = StateGraph(state)

    graph.add_node("classification_dialog_type", partial(base_nodes.classify_node, llm=classifier_llm))
    graph.add_node("search", partial(base_nodes.hybrid_search_node, vector_store=vector_store))
    graph.add_node("reranker", partial(base_nodes.rerank_docs_node, reranker=reranker, tokenizer=tokenizer))
    graph.add_node("response", partial(base_nodes.generate_response_node, llm=llm))
    graph.add_node("clarify", partial(base_nodes.clarify_node, llm=llm))
    graph.add_node("call_operator", partial(base_nodes.call_operator_node, llm=llm))
    graph.add_node("small_talk", partial(base_nodes.small_talk_node, llm=llm))

    graph.add_edge(START, "classification_dialog_type")
    # graph.add_edge("classification_dialog_type", "search")

    graph.add_conditional_edges(
        "classification_dialog_type",
        dialog_type_router,
        {"search": "search", "small_talk": "small_talk"}
    )
    graph.add_edge("search", "reranker")

    graph.add_conditional_edges(
        "reranker",
        confidence_router,
        {"response": "response",
         "clarify": "clarify",
         "call_operator": "call_operator"}
    )

    # end edges
    graph.add_edge("clarify", END)
    graph.add_edge("response", END)
    graph.add_edge("call_operator", END)
    graph.add_edge("small_talk", END)

    return graph.compile()
