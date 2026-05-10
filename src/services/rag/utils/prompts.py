import yaml
from pathlib import Path
import os

ROOT_PATH = os.getenv("PYTHONPATH")
BASE_PROMPTS_PATH = Path(ROOT_PATH) / 'config' / 'prompts' / 'classification.yaml'


def load_prompts(
        prompts_path: str = BASE_PROMPTS_PATH,
        encoding: str = 'utf-8') -> dict:
    with open(prompts_path, encoding=encoding) as f:
        return yaml.safe_load(f)
