from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, exists, delete, case, func
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

    async def get_analytics(self) -> dict:
        try:
            total_result = await self._session.execute(
                select(func.count()).select_from(DialogHistory)
            )
            total = total_result.scalar()

            auto_result = await self._session.execute(
                select(func.count()).where(DialogHistory.operator == False)
            )
            auto = auto_result.scalar()

            operator_result = await self._session.execute(
                select(func.count()).where(DialogHistory.operator == True)
            )
            operator_count = operator_result.scalar()

            by_type_result = await self._session.execute(
                select(DialogHistory.dialog_type, func.count().label("count"))
                .group_by(DialogHistory.dialog_type)
                .order_by(func.count().desc())
            )

            max_score_result = await self._session.execute(
                select(func.max(DialogHistory.score)).where(DialogHistory.score.isnot(None))
            )
            avg_score = max_score_result.scalar()
            by_type = [{"dialog_type": row[0], "count": row[1]} for row in by_type_result.all()]

            return {
                "total": total,
                "auto_handled": auto,
                "operator_handled": operator_count,
                "score": avg_score,
                "by_type": by_type,
            }
        except Exception:
            raise

    async def get_dialogs_filtered(
            self,
            user_id: int | None = None,
            dialog_type: str | None = None,
            operator: bool | None = None,
            limit: int = 20,
            offset: int = 0,
    ) -> tuple[list[DialogHistory], int]:
        query = select(DialogHistory)
        count_query = select(func.count()).select_from(DialogHistory)

        if user_id:
            query = query.where(DialogHistory.user_id == user_id)
            count_query = count_query.where(DialogHistory.user_id == user_id)
        if dialog_type:
            query = query.where(DialogHistory.dialog_type == dialog_type)
            count_query = count_query.where(DialogHistory.dialog_type == dialog_type)
        if operator is not None:
            query = query.where(DialogHistory.operator == operator)
            count_query = count_query.where(DialogHistory.operator == operator)

        query = query.order_by(DialogHistory.finished_at.desc()).limit(limit).offset(offset)

        result = await self._session.execute(query)
        count_result = await self._session.execute(count_query)

        return result.scalars().all(), count_result.scalar()
