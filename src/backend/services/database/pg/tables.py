from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func, String, JSON, TEXT, Integer, String, Float, Boolean, DateTime, ForeignKey, func
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    ...


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    source: Mapped[str] = mapped_column(nullable=True, unique=True)
    content: Mapped[str] = mapped_column(TEXT, nullable=False)

    doc_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True,
                                                         comment="дополнительная информация о документе")
    finished_at: Mapped[datetime] = mapped_column(server_default=func.now())


class DialogHistory(Base):
    __tablename__ = "dialog_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    dialog_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    operator: Mapped[bool] = mapped_column(Boolean, default=False)
    history: Mapped[dict] = mapped_column(JSON, nullable=False)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True,
                                                   comment='Уверенность ответа при ранжировании (max)')
    finished_at: Mapped[datetime] = mapped_column(server_default=func.now())
