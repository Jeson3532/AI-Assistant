from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DialogHistoryModel(BaseModel):
    user_id: int = Field(...)
    username: Optional[str] = Field(None)
    dialog_type: Optional[str] = Field(None)
    operator: bool = Field(False)
    history: list[dict] = Field(...)
