from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os
from src.backend import ROOT_PATH

env_file = str(ROOT_PATH / '.env')


class OllamaConfig(BaseSettings):
    OLLAMA_HOST: str = 'localhost'
    OLLAMA_PORT: int
    RERANKER_MODEL_NAME: str = 'BAAI/bge-reranker-v2-m3'

    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')

    @property
    def base_url(self):
        return f"http://{self.OLLAMA_HOST}:{self.OLLAMA_PORT}"



