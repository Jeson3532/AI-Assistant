from fastapi import APIRouter, Depends
from src.backend.schemas.history.response import AnalyticsResponse, PaginatedDialogHistory
from src.backend.dependencies.services import get_db_service
from src.backend.services.database.pg.pg_service import DatabaseService
from src.backend.services.database.pg.service import HistoryService
from src.backend.dependencies.auth import auth_user

router = APIRouter(prefix='/analytics', tags=['Analytics', 'Аналитика'])


@router.get("/", response_model=AnalyticsResponse)
async def get_analytics(
        authenticated: str = Depends(auth_user),
        db: DatabaseService = Depends(get_db_service)):
    service = HistoryService(db)
    return await service.get_analytics()


@router.get("/journal/", response_model=PaginatedDialogHistory)
async def get_journal(
        authenticated: str = Depends(auth_user),
        user_id: int | None = None,
        dialog_type: str | None = None,
        operator: bool | None = None,
        limit: int = 20,
        offset: int = 0,
        db: DatabaseService = Depends(get_db_service)):
    service = HistoryService(db)
    return await service.get_dialogs_filtered(
        user_id=user_id,
        dialog_type=dialog_type,
        operator=operator,
        limit=limit,
        offset=offset,
    )
