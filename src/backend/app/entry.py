from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.utils.log import logger
from src.services.rag.utils.prompts import load_prompts
from src.services.rag.db.base import load_vectorstore, load_client
from src.backend.routes import routers
from langchain_ollama import ChatOllama
from src.services.models.service import ModelService
from src.services.rag.graphs.build import build_graph
from src.services.rag.states.base import BasicState
from dotenv import load_dotenv
import torch

load_dotenv()
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.prompts = load_prompts()
    # Загрузка qdrant
    logger.info("Загрузка qdrant...")
    qdrant_client = load_client()
    vectorstore = load_vectorstore(qdrant_client)
    logger.info("Qdrant загружен...")

    # Инициализация моделей и сборка RAG-графа
    model_service = ModelService()

    # загрузка основной модели
    logger.info("Загрузка основной модели...")
    llm = model_service.load_model(model_name='qwen2.5:14b')
    logger.info("Основная модель загружена")
    logger.info("Warmup модели...")
    await model_service.warmup(llm)
    logger.info("Warmup модели завершен")
    # загрузка reranker + tokenizer
    logger.info("Загрузка reranker-model...")
    reranker, tokenizer = await model_service.load_reranker(device=DEVICE)
    logger.info("Reranker-model загружен")
    # сборка графа
    app.state.llm_graph = build_graph(reranker, tokenizer, BasicState, llm, vectorstore)

    logger.info("Загрузка роутеров...")
    for router in routers:
        app.include_router(router)
    logger.info("Загрузка роутеров завершена")

    logger.info("Backend up")
    yield
    qdrant_client.close()
    logger.info("Backend down")


app = FastAPI(
    title="AI Assistant Backend",
    version='v1.0',
    description="Серверная часть ассистента для digital-агенства",
    lifespan=lifespan
)
