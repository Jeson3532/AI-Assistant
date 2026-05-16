from langchain_core.language_models import BaseChatModel
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from src.backend.services.rag.utils.prompts import load_prompts
from langchain_core.messages.ai import AIMessage
from src.backend.utils.log import logger

prompts = load_prompts()
GENERATE_PROMPTS = prompts.get("generate", {})


async def generate_response(
        model: BaseChatModel,
        user_query: str,
        docs: list[Document],
        dialog_type: str = 'other'
):
    try:
        context = '\n'.join([doc.page_content for doc in docs])

        prompt = GENERATE_PROMPTS.get(dialog_type, None)
        if not prompt:
            prompt = GENERATE_PROMPTS.get("other")
        if not prompt:
            raise ValueError(f"Промт {dialog_type} не находится в файле с промтами")

        template = ChatPromptTemplate.from_template(prompt)
        chain = template | model

        response: AIMessage = await chain.ainvoke({"query": user_query, "context": context})
        return response
    except Exception as e:
        logger.error(f"{e.__class__.__name__} | Ошибка при генерации ответа от модели: {e}")
