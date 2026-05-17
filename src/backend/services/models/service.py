from .config import OllamaConfig
from langchain_ollama import ChatOllama
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import asyncio
from concurrent.futures import ThreadPoolExecutor


BASE_CONFIG = OllamaConfig()


class ModelService:
    def __init__(self, config=BASE_CONFIG):
        self._config = config
        self.executor = ThreadPoolExecutor(max_workers=2)

    def load_model(self, model_name: str, temperature: float, top_k: int = 1):
        llm = ChatOllama(
            model=model_name,
            base_url=self._config.base_url,
            temperature=temperature,
            top_k=1
        )
        return llm

    def process_load_reranker(self, device: str):
        tokenizer = AutoTokenizer.from_pretrained(self._config.RERANKER_MODEL_NAME)
        reranker = AutoModelForSequenceClassification.from_pretrained(self._config.RERANKER_MODEL_NAME).to(
            device).eval()
        return reranker, tokenizer

    async def load_reranker(self, device: str = 'cpu'):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.process_load_reranker, device)

    @staticmethod
    async def warmup(model: ChatOllama) -> None:
        try:
            await model.ainvoke("Это warmup, если готов начать работу - ответь одно слово true.")
        except Exception:
            raise
