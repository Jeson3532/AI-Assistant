from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from src.services.rag.db.config import QdrantConfig

config = QdrantConfig()


def create_collection(
        client: QdrantClient,
        collection_name: str = config.COLLECTION_NAME,
        timeout: int | None = None) -> None:
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=config.EMBEDDING_SIZE,
                distance=Distance.COSINE
            ),
            timeout=timeout
        )


if __name__ == '__main__':
    client = QdrantClient(
        url=config.url
    )

    create_collection(client=client)
