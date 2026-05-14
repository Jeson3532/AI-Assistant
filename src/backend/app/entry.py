from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.utils.log import logger
from src.services.rag.utils.prompts import load_prompts


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.prompts = load_prompts()

    logger.info("Backend up")
    yield
    logger.info("Backend down")


app = FastAPI(
    title="AI Assistant Backend",
    version='v1.0',
    description="Серверная часть ассистента для digital-агенства",
    lifespan=lifespan
)
