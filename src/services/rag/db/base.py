from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_ollama import OllamaEmbeddings
from langchain_core.embeddings import Embeddings
from src.services.rag.db.config import QdrantConfig
from langchain_qdrant import QdrantVectorStore

config = QdrantConfig()


def delete_collection(
        client: QdrantClient,
        collection_name: str = config.COLLECTION_NAME) -> None:
    if client.collection_exists(config.COLLECTION_NAME):
        client.delete_collection(collection_name=collection_name)


def create_collection(
        client: QdrantClient,
        collection_name: str = config.COLLECTION_NAME,
        timeout: int | None = None) -> None:
    if not client.collection_exists(config.COLLECTION_NAME):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=config.EMBEDDING_SIZE,
                distance=Distance.COSINE
            ),
            timeout=timeout
        )


def load_client(url: str = config.url) -> QdrantClient:
    return QdrantClient(url=url)


def load_vectorstore(
        client: QdrantClient,
        collection_name: str = config.COLLECTION_NAME,
        embed_func: Embeddings = config.embed_func) -> QdrantVectorStore:
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embed_func
    )


if __name__ == '__main__':
    main_client = load_client()
