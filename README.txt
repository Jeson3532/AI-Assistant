# AI-ассистент саппорта - Рецифра

**Стек:** _Python 3.12, FastAPI, LangGraph, Qdrant, PostgreSQL, Ollama, aiogram 3_
**CI/CD-стек:** _git, docker, alembic_

---

## Описание

Интеллектуальный ассистент службы поддержки digital-агентства **Рецифра**. Система автоматически классифицирует входящие обращения,
ищет релевантные ответы в базе знаний и либо отвечает автоматически, либо передаёт запрос живому оператору.
Позволяет сохранять всю статистику и анализировать результаты.

### Граф проекта

![RAG Pipeline](static/files/project_graph.png)

---

## Системные требования

| Параметр | Минимум | Рекомендуется |
|----------|---------|---------------|
| ОС | Ubuntu 20.04, Windows 10, macOS 11 | Ubuntu 22.04 |
| RAM | 8 GB | 16 GB+ |
| Диск | 20 GB | 40 GB+ |
| GPU | - | NVIDIA (CUDA) |

> Без GPU модели работают на CPU - первый запуск и инференс значительно медленнее.

---

## Установка и запуск

### Шаг 1 - Клонируйте репозиторий

```bash
git clone git@github.com:Jeson3532/AI-Assistant.git && cd AI-Assistant-main
```

### Шаг 2 - Установите Docker Desktop

Скачайте и установите: https://www.docker.com/products/docker-desktop/

```bash
docker --version
```

### Шаг 3 - Установите WSL *(только для Windows)*

```bash
wsl --install
```

После установки потребуется перезагрузка.

### Шаг 4 - Создайте файл `.env` в корне проекта

```env
# Qdrant vector DB
QDRANT_HOST=cdm-qdrant-main
QDRANT_PORT=6333
# Ollama
OLLAMA_HOST=cdm-ollama
OLLAMA_PORT=11434
# Postgres DB
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=dbname
POSTGRES_PORT=5432
# Telegram bot
BOT_TOKEN=your-bot-token
OPERATOR_IDS=[1234567890]
# Backend
BACKEND_URL=http://cdm-backend-main:8000
SECRET=your-secret
```

### Шаг 5 - Соберите и запустите контейнеры

```bash
docker compose up -d --build
```

> **Первая сборка занимает 15–40 минут** - скачиваются образы, модели BAAI/bge-m3, cross-encoder и веса Ollama.

Проверить статус:

```bash
docker ps
```

### Шаг 6 - Примените миграции

```bash
docker exec -it cdm-backend-main alembic upgrade head
```

### Шаг 7 - Загрузите модели в Ollama

**Если видеопамяти >=16:**
```bash
docker exec -it cdm-ollama ollama pull qwen2.5:1.5b
docker exec -it cdm-ollama ollama pull qwen2.5:7b
```
**Если видеопамяти >=12:**
```bash
docker exec -it cdm-ollama ollama pull qwen2.5:1.5b
docker exec -it cdm-ollama ollama pull qwen2.5:3b
```
**Если видеопамяти <12:**
```bash
docker exec -it cdm-ollama ollama pull qwen2.5:0.5b
docker exec -it cdm-ollama ollama pull qwen2.5:1.5b
```

> Ключевой момент: стабильность работы RAG-пайплайна напрямую зависит от того, как нейросеть сможет понять контекст запроса. Чем легче модель - тем хуже результат.
> **ВАЖНО!** Чтобы на стороне бекенда использовались именно Ваши модели, нужно в `src/backend/app/entry.py` внутри lifespan() отредактировать llm и classifier_llm (заменить на установленные model_name)
### Шаг 8 - Откройте документацию API

| Интерфейс | Адрес |
|-----------|-------|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## Использование

Фронтенд реализован как **Telegram-бот**. После запуска контейнеров найдите бота по токену и отправьте `/start`.

- Пользователь пишет вопрос - ассистент обрабатывает и отвечает
- При низкой уверенности задаёт уточняющий вопрос
- При очень низкой уверенности создаёт тикет и уведомляет оператора
- Оператор принимает тикет и ведёт переписку через бота (двусторонняя связь и синхронизация диалога)
- `/exit` - завершить диалог с ассистентом (история диалога сохраняется)
- `/close` - закрыть тикет оператором (история диалога сохраняется)

---

## Структура проекта

```
AI-Assistant-main/
│   docker-compose.yaml
│   alembic.ini
│
├── migrations/
│   └── versions/
│
└── src/
    ├── backend/
    │   ├── app/
    │   │   ├── entry.py          # Точка входа FastAPI, инициализация RAG
    │   │   └── exceptions.py     # Обработчики ошибок
    │   │
    │   ├── tests/  # Авто-тесты (API)
    │   │
    │   ├── config/
    │   │   └── prompts.yaml      # Промпты для всех типов обращений
    │   │
    │   ├── dependencies/
    │   │   ├── auth.py           # X-API-Key аутентификация
    │   │   ├── rag.py            # Dependency injection RAG-компонентов
    │   │   └── services.py       # Dependency injection DB-сервисов
    │   │
    │   ├── routes/
    │   │   ├── assistant.py      # POST /assistant/, /assistant/stream/
    │   │   ├── docs.py           # POST/GET /docs/
    │   │   ├── history.py        # POST/GET /history/
    │   │   └── analytics.py      # GET /analytics/, /analytics/journal/
    │   │
    │   ├── schemas/              # Pydantic-схемы валидации
    │   ├── services/
    │   │   ├── database/pg/      # PostgreSQL: engine, tables, репозитории
    │   │   ├── models/           # Загрузка LLM и reranker
    │   │   └── rag/
    │   │       ├── graphs/       # Сборка LangGraph-графа
    │   │       ├── nodes/        # Узлы графа (classify, search, rerank, generate)
    │   │       ├── search/       # Гибридный поиск + cross-encoder reranker
    │   │       ├── splitters/    # Разбивка документов на чанки
    │   │       └── db/           # Qdrant клиенты и векторное хранилище
    │   └── utils/
    │
    ├── frontend/
    │   └── bot/
    │       ├── app.py            # Точка входа aiogram
    │       ├── routers/          # Message и callback роутеры
    │       ├── fsm/              # FSM-состояния диалога
    │       ├── keyboards/        # Inline-клавиатуры
    │       ├── storage/          # In-memory хранилище тикетов
    │       ├── templates/        # Шаблоны сообщений и форматирование
    │       └── utils/request.py  # HTTP-клиент к бэкенду
```

---

## Описание модулей

**BACKEND:**
- `src/backend/app/entry.py` - точка входа FastAPI, lifespan-инициализация всех компонентов RAG
- `src/backend/config/prompts.yaml` - специализированные промпты для каждой из 10 категорий обращений
- `src/backend/routes/assistant.py` - эндпоинты запроса к ассистенту (обычный и SSE-стриминг)
- `src/backend/routes/analytics.py` - статистика и журнал обращений с фильтрами и пагинацией
- `src/backend/services/rag/graphs/` - сборка LangGraph-графа с conditional edges
- `src/backend/services/rag/nodes/` - реализация каждого узла графа
- `src/backend/services/rag/search/` - гибридный поиск (dense + BM25) и cross-encoder реранкер
- `src/backend/tests/` - тестирование API.

**FRONTEND:**
- `src/frontend/bot/routers/message/assistant.py` - обработка сообщений, стриминг статусов, создание тикетов
- `src/frontend/bot/routers/message/operator.py` - приём и закрытие тикетов оператором
- `src/frontend/bot/routers/callback/assistant.py` - аналитика и журнал через inline-кнопки
- `src/frontend/bot/storage/tickets.py` - in-memory хранилище активных тикетов

**SERVICES:**
- `src/backend/services/models/` - загрузка и warmup LLM (Ollama), cross-encoder reranker (HuggingFace)
- `src/backend/services/database/pg/` - PostgreSQL: async engine, ORM-таблицы, репозитории, сервисный слой

---

## Список эндпоинтов

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/assistant/` | Запрос к ассистенту, синхронный ответ |
| POST | `/assistant/stream/` | Запрос к ассистенту, SSE-стриминг статусов |
| POST | `/docs/` | Загрузка документа в базу знаний |
| GET | `/docs/` | Просмотр коллекции векторной БД |
| POST | `/history/` | Сохранение истории диалога |
| GET | `/history/` | Получение всех диалогов |
| GET | `/analytics/` | Сводная статистика (всего, авто, оператор, по типам) |
| GET | `/analytics/journal/` | Журнал обращений с фильтрами и пагинацией |

> Все эндпоинты защищены заголовком `X-Secret-Key` (Базовая защита для MVP).

---

## Используемые ML-модели

| Модель                                 | Назначение                                     | Устройство |
|----------------------------------------|------------------------------------------------|------------|
| `qwen2.5:1.5b` (Ollama)                | Классификация типа обращения                   | CPU / GPU |
| `qwen2.5:3b` (Ollama)                  | Основная response-модель для генерации ответов | CPU / GPU |
| `BAAI/bge-m3`                          | Dense-эмбеддинги для векторного поиска         | CPU / GPU |
| `Qdrant/BM25` (FastEmbed)              | Sparse-эмбеддинги для гибридного поиска        | CPU |
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | Реранкинг результатов поиска (ранжирование)    | CPU / GPU |

---

## Ограничения текущего прототипа

- Telegram-бот как фронтенд не является полноценным веб-интерфейсом (REST API позволяет подключить любой клиент), он используется только для быстрой визуализации прототипа.
- Модели `qwen2.5:1.5b` и `qwen2.5:3b`- очень лёгкие, подходят для прототипа. Для production-среды рекомендуется более крупная модель (14b для response и 3b-7b для классификации диалога)
- In-memory хранилище тикетов сбрасывается при перезапуске контейнера

---

## Возможные проблемы

### Порт 8000 уже занят

```bash
# macOS / Linux
lsof -i :8000

# Windows
netstat -ano | findstr :8000
```

Или измените порт в `docker-compose.yaml` на `8001:8000`.

### Контейнер не запускается

```bash
docker compose logs -f
```

### Ollama не скачала модель

```bash
docker exec -it cdm-ollama ollama list
docker exec -it cdm-ollama ollama pull qwen2.5:<ваши веса>
```

### Недостаточно памяти

Откройте **Docker Desktop → Settings → Resources** и увеличьте RAM до 8 GB+.

### WSL не установлен *(Windows)*

Запустите терминал от имени администратора:

```bash
wsl --install
```

---

## Остановка

```bash
docker compose down
```