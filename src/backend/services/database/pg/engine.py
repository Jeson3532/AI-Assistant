from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.backend.services.database.pg.tables import Base
from sqlalchemy import text

from src.backend.services.database.pg.config import DBConfig

cfg = DBConfig()

engine = create_async_engine(
    cfg.get_url(driver='asyncpg'),
    pool_size=cfg.POOL_SIZE,
    max_overflow=cfg.POOL_OVERFLOW,
    pool_timeout=cfg.POOL_TIMEOUT
)
session_fabric = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with session_fabric() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
