from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, exists, delete
from sqlalchemy.exc import IntegrityError
from src.backend.services.database.pg.tables import KnowledgeBase, DialogHistory
from src.backend.schemas.history.input import DialogHistoryModel


class DatabaseService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self.history = HistoryRepo(session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def refresh(self, obj):
        await self._session.refresh(obj)


class HistoryRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_dialog(self, dialog: DialogHistory) -> DialogHistory:
        try:
            self._session.add(dialog)
            return dialog
        except Exception:
            await self._session.rollback()
            raise

    async def get_all_dialogs(self) -> list[DialogHistory]:
        try:
            result = await self._session.execute(
                select(DialogHistory).order_by(DialogHistory.finished_at.desc())
            )
            return result.scalars().all()
        except Exception:
            raise

    async def get_dialogs_by_user(self, user_id: int) -> list[DialogHistory]:
        try:
            result = await self._session.execute(
                select(DialogHistory)
                .where(DialogHistory.user_id == user_id)
                .order_by(DialogHistory.finished_at.desc())
            )
            return result.scalars().all()
        except Exception:
            raise
