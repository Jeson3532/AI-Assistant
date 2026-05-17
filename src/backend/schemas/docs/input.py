from pydantic import BaseModel, Field


class UploadDocsModel(BaseModel):
    title: str = Field(..., description="Краткое описание документа")
    content: str = Field(..., description="Содержимое документа")
    type: str = Field(..., description="Тип документа")
    chunk_size: int = Field(500, description="Размер одного чанка при сплите")



