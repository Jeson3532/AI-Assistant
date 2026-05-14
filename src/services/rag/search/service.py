from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.models import Filter, FieldCondition, MatchValue


def get_filter(dialog_type: str):
    return Filter(must=[FieldCondition(
        key="metadata.dialog_type",
        match=MatchValue(value=dialog_type))])


async def hybrid_search(
        vector_store: QdrantVectorStore,
        user_query: str,
        dialog_type: str = 'other',
        k: int = 20
):
    return await vector_store.asimilarity_search(
        query=user_query,
        filter=get_filter(dialog_type),
        k=k
    )
