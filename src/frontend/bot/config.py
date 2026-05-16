from pydantic_settings import BaseSettings, SettingsConfigDict
from src.frontend import ROOT_PATH
from dotenv import load_dotenv
import os

load_dotenv()
env_path = str(ROOT_PATH / '.env')


class BotConfig(BaseSettings):
    BOT_TOKEN: str = None
    OPERATOR_IDS: list[int] = []

    model_config = SettingsConfigDict(env_file=env_path, extra='ignore')

    @property
    def token(self):
        return self.BOT_TOKEN
