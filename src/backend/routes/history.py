from fastapi import APIRouter, Depends
from src.backend.services.database.pg.pg_service import DatabaseService
from sqlalchemy import select
from src.backend.schemas.history.input import DialogHistoryModel
from src.backend.schemas.history.response import DialogHistoryResponse
from src.backend.dependencies.services import get_db_service
from src.backend.services.database.pg.service import HistoryService
from src.backend.schemas.history.response import DialogHistoryResponse, AnalyticsResponse
from src.backend.schemas.history.response import DialogHistoryResponse, AnalyticsResponse, PaginatedDialogHistory

router = APIRouter(prefix='/history', tags=['History', 'История диалогов'])


@router.post("/")
async def save_dialog(
        body: DialogHistoryModel,
        db: DatabaseService = Depends(get_db_service)):
    service = HistoryService(db)
    return await service.save_dialog(body)


@router.get("/", response_model=list[DialogHistoryResponse])
async def get_dialogs(
        db: DatabaseService = Depends(get_db_service)):
    service = HistoryService(db)
    return await service.get_dialogs()

