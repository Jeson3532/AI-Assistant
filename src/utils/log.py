import logging
import os
from pathlib import Path
from src import ROOT_PATH

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub.utils._http").setLevel(logging.ERROR)
logging.getLogger("pyannote").setLevel(logging.ERROR)

BASE_LOGS_DIR = str(ROOT_PATH / "logs")


if not os.path.exists(BASE_LOGS_DIR):
    os.makedirs(BASE_LOGS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path(BASE_LOGS_DIR) / 'main.log'),
    ]
)
logger = logging.getLogger(__name__)