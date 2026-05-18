from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.backend.utils.log import logger
from src.backend.services.rag.utils.prompts import load_prompts
from src.backend.services.rag.db.base import load_vectorstore, load_client, load_async_client
from src.backend.routes import routers
from src.backend.services.models.service import ModelService
from src.backend.services.rag.graphs.build import build_graph
from src.backend.services.rag.states.base import BasicState
from src.backend.app.exceptions import setup_exceptions
from src.backend.services.database.pg.engine import init_db
from dotenv import load_dotenv

import torch

load_dotenv()
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


@asynccontextmanager
async def lifespan(app: FastAPI):
    # блок работы с инициализацией инструментов RAG-пайплайна
    app.state.prompts = load_prompts()
    logger.info("Загрузка qdrant...")
    # загрузка клиентов
    logger.info("Загрука клиентов...")
    qdrant_client = load_client()
    async_qdrant_client = load_async_client()
    vectorstore = load_vectorstore(qdrant_client)
    logger.info("Клиенты загружены")

    # запись клиентов
    app.state.qdrant_vectorstore = vectorstore
    app.state.qdrant_async_client = async_qdrant_client
    logger.info("Qdrant загружен...")

    # инициализация моделей и сборка RAG-графа
    model_service = ModelService()

    # загрузка основной модели
    logger.info("Загрузка ML-моделей...")
    llm = model_service.load_model(model_name='qwen2.5:3b', temperature=0.7, top_k=40)
    classifier_llm = model_service.load_model(model_name="qwen2.5:1.5b", temperature=0.0)

    logger.info("Основная модель загружена")
    logger.info("Warmup моделей...")
    await model_service.warmup(llm)
    await model_service.warmup(classifier_llm)
    logger.info("Warmup моделей завершен")
    # загрузка reranker + tokenizer
    logger.info("Загрузка reranker-model...")
    reranker, tokenizer = await model_service.load_reranker(device=DEVICE)
    logger.info("Reranker-model загружен")
    logger.info(f"DEVICE: {DEVICE}")
    # сборка графа
    app.state.llm_graph = build_graph(reranker, tokenizer, BasicState, llm, classifier_llm, vectorstore)

    # блок компонентов FastAPI
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

# excps
setup_exceptions(app)
