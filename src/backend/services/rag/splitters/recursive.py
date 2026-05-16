from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
import json
import hashlib
import uuid
from src.backend.exc import FailUploadDocument

from src.backend.utils.log import logger


def get_content_id(content: str, encoding: str = 'utf-8') -> str:
    hash_b = hashlib.md5(content.encode(encoding)).digest()
    return str(uuid.UUID(bytes=hash_b[:16]))


def load_json_document(
        vector_db: QdrantVectorStore,
        file_path: str,
        chunk_size=500,
        encoding: str = 'utf-8'):
    with open(file_path, 'r', encoding=encoding) as f:
        json_file = json.load(f)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_size // 10
    )
    try:
        docs = [
            Document(
                page_content=item['content'],
                metadata=item['metadata']
            ) for item in json_file]
    except (KeyError, TypeError) as e:
        logger.error(f"{e.__class__.__name__} | Загружен некорректный JSON. Traceback: {e}")
        return

    try:
        chunks = splitter.split_documents(docs)

        ids = [get_content_id(chunk.page_content) for chunk in chunks]  # перезапись, если уже существует
        vector_db.add_documents(documents=chunks, ids=ids)
    except Exception as e:
        logger.error(f"{e.__class__.__name__} | Общая ошибка при добавлении документов в базу. Traceback: {e}")
        return


def load_dict_document(
        vector_db: QdrantVectorStore,
        records: list[dict],
        chunk_size=500) -> None:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_size // 10
    )
    try:
        docs = [
            Document(
                page_content=item['content'],
                metadata=item['metadata']
            ) for item in records]
    except (KeyError, TypeError) as e:
        logger.error(f"{e.__class__.__name__} | Загружен некорректный list[dict]. Traceback: {e}")
        return

    try:
        chunks = splitter.split_documents(docs)

        ids = [get_content_id(chunk.page_content) for chunk in chunks]  # перезапись, если уже существует
        vector_db.add_documents(documents=chunks, ids=ids)
    except Exception as e:
        logger.error(f"{e.__class__.__name__} | Общая ошибка при добавлении документов в базу. Traceback: {e}")
        raise FailUploadDocument("Ошибка при загрузке документа") from e


