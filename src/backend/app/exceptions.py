from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.backend import exc


def setup_exceptions(app: FastAPI) -> None:
    @app.exception_handler(exc.BaseDocumentError)
    async def _(request: Request, exception: exc.BaseDocumentError):
        return JSONResponse(
            status_code=500,
            content={"detail": "Ошибка при загрузке документа, попробуйте позже"}
        )


