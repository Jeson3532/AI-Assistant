from langchain_core.documents import Document
from langchain_core.messages.ai import AIMessage
from typing import TypedDict
from typing import Literal


class BasicState(TypedDict):
    query: str
    dialog_type: str
    docs: list[Document]
    reranked_docs: list[Document]
    rerank_scores: list[float]
    response: AIMessage | None
    operator: bool
    history: list[dict]
