from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

root_path = Path(os.getenv("PYTHONPATH"))
env_file = str(root_path / '.env')


class QdrantConfig(BaseSettings):
    QDRANT_HOST: str = 'localhost'
    QDRANT_PORT: str
    COLLECTION_NAME: str = 'vector_db'
    EMBEDDING_SIZE: int = 1536

    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')

    @property
    def url(self):
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"
