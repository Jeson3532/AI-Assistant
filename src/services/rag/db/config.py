from pydantic_settings import BaseSettings, SettingsConfigDict
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import os
from pathlib import Path
from langchain_core.embeddings import Embeddings
from langchain_ollama import OllamaEmbeddings
from src import ROOT_PATH
from functools import cached_property

env_file = str(ROOT_PATH / '.env')


class QdrantConfig(BaseSettings):
    QDRANT_HOST: str = 'localhost'
    QDRANT_PORT: str
    COLLECTION_NAME: str = 'vector_db'
    EMBEDDING_SIZE: int = 1024
    EMBEDDING_MODEL: str = 'BAAI/bge-m3'

    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')

    @property
    def url(self):
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    @cached_property
    def embed_func(self) -> Embeddings:
        return HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={"device": "cuda"},
            encode_kwargs={"normalize_embeddings": True}
        )
