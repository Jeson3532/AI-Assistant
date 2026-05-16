import yaml
from pathlib import Path
import os
from functools import lru_cache
from src.backend import ROOT_PATH

BASE_PROMPTS_PATH = Path(ROOT_PATH) / 'config' / 'prompts.yaml'



@lru_cache(maxsize=1)
def load_prompts(
        prompts_path: str = BASE_PROMPTS_PATH,
        encoding: str = 'utf-8') -> dict:
    with open(prompts_path, encoding=encoding) as f:
        return yaml.safe_load(f)
