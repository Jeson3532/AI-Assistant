from langchain_core.language_models import BaseChatModel
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessage
from src.backend.services.rag.utils.prompts import load_prompts
from src.backend.utils.log import logger

prompts = load_prompts()
GENERATE_PROMPTS = prompts.get("generate", {})


async def generate_response(
        model: BaseChatModel,
        prompt: str | None,
        user_query: str,
        docs: list[Document],
        dialog_type: str = 'other',
        history: list[dict] = None
):
    try:
        context = '\n'.join([doc.page_content for doc in docs])
        if not prompt:
            prompt = GENERATE_PROMPTS.get(dialog_type, None)
            if not prompt:
                prompt = GENERATE_PROMPTS.get("other")
            if not prompt:
                raise ValueError(f"Промт {dialog_type} не находится в файле с промтами")
        # logger.info(f"ИСПОЛЬЗУЕМЫЙ ПРОМТ: {prompt}")
        messages = [SystemMessage(content=prompt.format_map({
            "query": user_query,
            "context": context
        }))]

        # история диалога
        for msg in (history or []):
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['text']))
            else:
                messages.append(AIMessage(content=msg['text']))

        # текущий вопрос
        messages.append(HumanMessage(content=user_query))

        response: AIMessage = await model.ainvoke(messages)
        return response
    except Exception as e:
        logger.error(f"{e.__class__.__name__} | Ошибка при генерации ответа от модели: {e}")
