from fastapi import APIRouter, Depends
from src.backend.services.database.pg.pg_service import DatabaseService
from src.backend.schemas.history.input import DialogHistoryModel
from src.backend.dependencies.services import get_db_service
from src.backend.services.database.pg.service import HistoryService
from src.backend.dependencies.auth import auth_user
from src.backend.schemas.history.response import DialogHistoryResponse, AnalyticsResponse, PaginatedDialogHistory

router = APIRouter(prefix='/history', tags=['History', 'История диалогов'])


@router.post("/")
async def save_dialog(
        body: DialogHistoryModel,
        db: DatabaseService = Depends(get_db_service),
        authenticated: str = Depends(auth_user)):
    service = HistoryService(db)
    return await service.save_dialog(body)


@router.get("/", response_model=list[DialogHistoryResponse])
async def get_dialogs(
        db: DatabaseService = Depends(get_db_service),
        authenticated: str = Depends(auth_user)):
    service = HistoryService(db)
    return await service.get_dialogs()

