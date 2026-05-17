from enum import Enum


class NodeStatus(str, Enum):
    classification_dialog_type = "🔍 <b>Определяем тип обращения...</b>"
    search = "📚 <b>Ищем ответ в базе знаний...</b>"
    reranker = "⚙️ <b>Готовим результаты...</b>"
    response = "✍️ <b>Формируем ответ...</b>"
    clarify = "🤔 <b>Уточняем детали...</b>"
    call_operator = "👨‍💼 <b>Передаём менеджеру...</b>"
    small_talk = "💬 <b>Отвечаем...</b>"


FINAL_NODES = {
    NodeStatus.response,
    NodeStatus.clarify,
    NodeStatus.call_operator,
    NodeStatus.small_talk,
}