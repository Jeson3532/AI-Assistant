FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV TORCH_HOME=/app/models

COPY src/backend/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY src/backend /app/src

CMD ["uvicorn", "src.backend.app.entry:app", "--host", "0.0.0.0", "--port", "8000"]