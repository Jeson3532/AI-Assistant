from fastapi import HTTPException, Header, Security
from fastapi.security import APIKeyHeader
from secrets import compare_digest
import os

api_key_header = APIKeyHeader(name="x-secret-key", auto_error=True)


def auth_user(x_secret_key: str = Security(api_key_header)):
    backend_secret = os.getenv("SECRET")
    if not compare_digest(x_secret_key, backend_secret):
        raise HTTPException(status_code=401, detail="Нет доступа")