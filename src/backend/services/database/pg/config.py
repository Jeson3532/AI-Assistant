from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os
from src.backend import ROOT_PATH

env_file = str(ROOT_PATH / '.env')


class DBConfig(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = 'postgres-main'
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POOL_SIZE: int = 16
    POOL_OVERFLOW: int = 20
    POOL_TIMEOUT: int = 30
    BOT_TOKEN: str = None

    model_config = SettingsConfigDict(env_file=env_file, extra='ignore')

    @property
    def base_url(self):
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def get_url(self, driver: str = 'asyncpg'):
        return f"postgresql+{driver}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

