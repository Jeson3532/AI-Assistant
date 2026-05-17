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
