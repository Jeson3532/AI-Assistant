from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.services.database.pg.engine import get_session
from src.backend.services.database.pg.pg_service import DatabaseService


def get_db_service(session: AsyncSession = Depends(get_session)):
    return DatabaseService(session=session)
