from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DialogHistoryResponse(BaseModel):
    id: int
    user_id: int
    username: Optional[str]
    dialog_type: Optional[str]
    operator: bool
    history: list[dict]
    finished_at: datetime

    class Config:
        from_attributes = True


class DialogTypeStats(BaseModel):
    dialog_type: Optional[str]
    count: int


class AnalyticsResponse(BaseModel):
    total: int
    auto_handled: int
    operator_handled: int
    by_type: list[DialogTypeStats]


class PaginatedDialogHistory(BaseModel):
    items: list[DialogHistoryResponse]
    total: int
    limit: int
    offset: int
