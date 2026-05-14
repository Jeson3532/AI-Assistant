from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages.ai import AIMessage
import yaml
from langchain_core.language_models import BaseChatModel
from src.utils.log import logger
from src.services.rag.utils.prompts import load_prompts

prompts = load_prompts()


async def get_dialog_type(
        model: BaseChatModel,
        user_query: str,
        prompt_name: str = 'classify_intent') -> str:
    try:
        prompt = prompts.get(prompt_name)
        if not prompt:
            raise ValueError("Ошибка при передаче промта: промт не найден")
        template = ChatPromptTemplate.from_template(prompt)
        chain = template | model

        response: AIMessage = await chain.ainvoke({"query": user_query})
        if not response:
            return "other"
        return response.content.strip().lower()
    except Exception as e:
        logger.error(f"{e.__class__.__name__} | Ошибка при попытке получить тип диалога: {e}")
        return 'other'
