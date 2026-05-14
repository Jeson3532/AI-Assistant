from qdrant_client import QdrantClient, AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, SparseVectorParams, SparseIndexParams
from langchain_ollama import OllamaEmbeddings
from langchain_core.embeddings import Embeddings
from src.services.rag.db.config import QdrantConfig
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from src.utils.log import logger

config = QdrantConfig()


def delete_collection(
        client: QdrantClient,
        collection_name: str) -> None:
    if client.collection_exists(collection_name):
        client.delete_collection(collection_name=collection_name)
        logger.info(f"Коллекция {collection_name} удалена")


def create_collection(
        client: QdrantClient,
        collection_name: str,
        timeout: int | None = None) -> None:
    if not client.collection_exists(collection_name):
        logger.info(f"Создание новой коллекции...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=config.EMBEDDING_SIZE,
                distance=Distance.COSINE
            ),
            sparse_vectors_config={
                "langchain-sparse": SparseVectorParams(
                    index=SparseIndexParams(on_disk=False)
                )
            },
            timeout=timeout
        )
        logger.info(f"Коллекция {collection_name} создана")


def load_client(url: str = config.url) -> QdrantClient:
    return QdrantClient(url=url)


def load_async_client(url: str = config.url) -> AsyncQdrantClient:
    return AsyncQdrantClient(url=url)


def load_vectorstore(
        client: QdrantClient,
        collection_name: str = config.COLLECTION_NAME,
        sparse_embeddings_model: str = 'Qdrant/BM25',
        embed_func: Embeddings = config.embed_func) -> QdrantVectorStore:
    if not client.collection_exists(collection_name):
        create_collection(client, collection_name)

    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embed_func,
        sparse_embedding=FastEmbedSparse(model_name=sparse_embeddings_model),
        retrieval_mode=RetrievalMode.HYBRID,
        validate_collection_config=False
    )


if __name__ == '__main__':
    ...
    # main_client = load_client()
    # delete_collection(main_client, config.COLLECTION_NAME)
    # create_collection(main_client, config.COLLECTION_NAME)
