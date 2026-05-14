from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings

root_path = Path(os.getenv("PYTHONPATH"))
env_file = str(root_path / '.env')


class QdrantConfig(BaseSettings):
    QDRANT_HOST: str = 'localhost'
    QDRANT_PORT: str
    COLLECTION_NAME: str = 'vector_db'
    EMBEDDING_SIZE: int = 1024
    EMBEDDING_MODEL: str = 'bge-m3'

    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')

    @property
    def url(self):
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    @property
    def embed_func(self) -> Embeddings:
        return OllamaEmbeddings(model=self.EMBEDDING_MODEL)
