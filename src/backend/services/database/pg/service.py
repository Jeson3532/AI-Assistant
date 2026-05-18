from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.services.database.pg.pg_service import DatabaseService
from src.backend.schemas.history.input import DialogHistoryModel
from src.backend.services.database.pg.tables import DialogHistory
from src.backend.utils.log import logger
from typing import Optional


class HistoryService:
    def __init__(self, db: DatabaseService):
        self._db = db

    async def save_dialog(self, data: DialogHistoryModel) -> DialogHistory:
        try:
            dialog = DialogHistory(
                user_id=data.user_id,
                username=data.username,
                dialog_type=data.dialog_type,
                operator=data.operator,
                score=data.score,
                history=data.history
            )
            await self._db.history.save_dialog(dialog)
            await self._db.commit()
            await self._db.refresh(dialog)
            return dialog
        except Exception as e:
            logger.error(f"Общая ошибка в {self.__class__.__name__}. Traceback: {e}")
            raise

    async def get_dialogs(self, user_id: int | None = None) -> list[DialogHistory]:
        try:
            if user_id:
                return await self._db.history.get_dialogs_by_user(user_id)
            return await self._db.history.get_all_dialogs()
        except Exception as e:
            logger.error(f"Общая ошибка в {self.__class__.__name__}. Traceback: {e}")
            raise

    async def get_analytics(self) -> dict:
        try:
            return await self._db.history.get_analytics()
        except Exception as e:
            logger.error(f"Общая ошибка в {self.__class__.__name__}. Traceback: {e}")
            raise

    async def get_dialogs_filtered(
            self,
            user_id: int | None = None,
            dialog_type: str | None = None,
            operator: bool | None = None,
            limit: int = 20,
            offset: int = 0,
    ) -> dict:
        try:
            items, total = await self._db.history.get_dialogs_filtered(
                user_id=user_id,
                dialog_type=dialog_type,
                operator=operator,
                limit=limit,
                offset=offset,
            )
            return {"items": items, "total": total, "limit": limit, "offset": offset}
        except Exception as e:
            logger.error(f"Общая ошибка в {self.__class__.__name__}. Traceback: {e}")
            raise
