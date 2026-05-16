FROM python:3.12-slim

WORKDIR /app

COPY src/frontend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/frontend /app/src

CMD ["python", "-m", "src.frontend.bot.app"]