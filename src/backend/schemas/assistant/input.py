from pydantic import BaseModel, Field


class SendQueryModel(BaseModel):
    query: str = Field(..., description="Запрос пользователя к ассистенту")
