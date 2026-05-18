from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DialogHistoryModel(BaseModel):
    user_id: int = Field(...)
    username: Optional[str] = Field(None)
    dialog_type: Optional[str] = Field(None)
    operator: bool = Field(False)
    score: Optional[float] = Field(None)
    history: list[dict] = Field(...)
