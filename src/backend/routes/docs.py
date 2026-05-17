from fastapi import APIRouter, Depends
from src.backend.schemas.docs.input import UploadDocsModel
from src.backend.services.rag.splitters.recursive import load_dict_document
from src.backend.services.rag.methods.docs import get_collection_data
from src.backend.dependencies.rag import get_vectorstore, get_async_client
from qdrant_client import AsyncQdrantClient
from src.backend.dependencies.auth import auth_user
from langgraph.graph.state import CompiledStateGraph

router = APIRouter(prefix='/docs', tags=['Documents', 'Документы'])


@router.post("/")
async def upload_docs(
        body: UploadDocsModel,
        vectorstore=Depends(get_vectorstore),
        authenticated: str = Depends(auth_user)):
    record = [{
        "content": body.content,
        "metadata": {
            "title": body.title,
            "dialog_type": body.type
        }
    }]
    load_dict_document(vectorstore, record, chunk_size=body.chunk_size)
    return {"success": True}


@router.get("/")
async def get_docs(
        collection_name: str,
        async_client: AsyncQdrantClient = Depends(get_async_client),
        authenticated: str = Depends(auth_user)):
    return await get_collection_data(async_client, collection_name=collection_name)
