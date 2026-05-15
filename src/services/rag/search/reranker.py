import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from langchain_core.documents import Document
from src.services.models.service import ModelService
from src.utils.log import logger

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


@torch.no_grad()
def rerank_docs(
        reranker,
        tokenizer,
        query: str,
        docs: list[Document] ,
        top_k: int = 5,
        threshold: float = 0.0
) -> tuple[list[Document], list[float]]:
    pairs = [[query, doc.page_content] for doc in docs]
    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors='pt',
        max_length=512
    )
    logger.info("Работает Reranker!")
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}  # чище чем цикл

    scores = reranker(**inputs, return_dict=True).logits.view(-1).float()
    probs = torch.sigmoid(scores)

    ranked = sorted(
        zip(probs.tolist(), docs),
        key=lambda x: x[0],
        reverse=True
    )
    # фильтр по порогу (возможно уберу)
    rel_docs_scores = [(doc, prob) for prob, doc in ranked[:top_k] if prob > threshold]

    rel_docs = [doc for doc, _ in rel_docs_scores]
    out_scores = [score for _, score in rel_docs_scores]
    logger.info("Reranker закончил работу!")
    return rel_docs, out_scores
