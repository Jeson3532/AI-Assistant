from pydantic import BaseModel, Field


class HistoryMessage(BaseModel):
    role: str
    text: str


class SendQueryModel(BaseModel):
    query: str = Field(..., description="Запрос пользователя к ассистенту")
    history: list[HistoryMessage] = Field(default_factory=list, description="История диалога")
