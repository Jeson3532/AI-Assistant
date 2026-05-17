from .assistant import router as assistant_router
from .docs import router as docs_router
from .history import router as history_router
from fastapi import APIRouter

routers = [v for v in list(globals().values()) if isinstance(v, APIRouter)]
