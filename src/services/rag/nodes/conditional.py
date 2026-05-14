from src.services.rag.states.base import BasicState


def confidence_router(state: BasicState):
    scores = state['rerank_scores']
    if not scores:
        return "call_operator"

    max_score = max(scores)
    if not scores or max_score < 0.3:
        return "call_operator"

    if max_score < 0.5:
        return "clarify"

    return "response"
