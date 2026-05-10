### План проекта
1. Инициализация QectorClient + QectorStore
2. Создание рекурсивного добавления JSON-документов в базу в формате списка с полями content, metadata
3. Классификация intent — определяем тип запроса перед поиском (task_status, technical_error, access и т.д.) через быстрый LLM-вызов
4. Гибридный поиск — dense + sparse (BM25) + RRF fusion. Настройка RetrievalMode.HYBRID в QdrantVectorStore
5. Re-ranking — берём топ-20 чанков, прогоняем через cross-encoder, оставляем топ-5
6. Генерация ответа — intent-специфичный промпт + топ-5 чанков → LLM → ответ
7. LangGraph оркестрация — собираем всё в граф:
START → classify_intent → hybrid_search → rerank → generate → END
8. API — FastAPI эндпоинт принимает запрос, прогоняет через граф, возвращает ответ