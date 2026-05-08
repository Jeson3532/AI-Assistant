from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, String, JSON, TEXT, Integer, String, Float, Boolean, DateTime, ForeignKey, func
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    ...


class Users(Base):
    __tablename__ = "knowledge_base"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    source: Mapped[str] = mapped_column(nullable=True, unique=True)
    content: Mapped[str] = mapped_column(TEXT, nullable=False)

    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True,
                                                     comment="дополнительная информация о документе")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
