from pydantic import BaseModel


class AssistantResponse(BaseModel):
    id: str
    query: str
    dialog_type: str | None
    operator: bool
    model_response: str
