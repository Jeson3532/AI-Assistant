from src.services.rag.splitters.recursive import load_json_document
from src.services.rag.search.service import hybrid_search
from src.services.rag.db.base import load_vectorstore, load_client
from src.services.rag.methods.type_classification import get_dialog_type
from src.services.rag.search.reranker import rerank_docs

from langchain_ollama import ChatOllama
from src.services.rag.graphs.build import build_graph
from src.services.rag.states.base import BasicState

from pprint import pp
import os
import pathlib
from src.utils.log import logger

# Загрузка qdrant
# client = load_client()
# vectorstore = load_vectorstore(client)
#
#
# # Загрузка документов
# load_json_document(vectorstore, file_path='files/example.json')
#
# # Проверка гибридного поиска
# user_query = "Добавили блок с партнерами?"
# dialog_type = get_dialog_type(llm, user_query)
#
# result = hybrid_search(vectorstore, user_query, dialog_type=dialog_type)
#
# logger.info(f"Тип диалога: {dialog_type}")
#
#
# reranked_docs = rerank_docs(user_query, result)
# print("Результат после реранкера:")
# for doc in reranked_docs:
#     print(doc.page_content)
# Загрузка LLM
# llm = ChatOllama(
#     model='qwen2.5:14b'
# )


# graph = build_graph(BasicState, llm, vectorstore)
#
# user_query = "что по правкам на основной странице?"
# response = graph.invoke({"query": user_query})
# pp(response)
