START_MESSAGE = "👋 Привет! Я <b>ассистент Рецифры</b> для оперативного решения задач в digital-агенстве.\nВыбери то, что тебя интересует:"
ASSISTANT_START_MESSAGE = "🤖 Вы перешли в чат с нейросетевым ассистентом.\nЗадайте интересующий Вас вопрос и получите на него ответ. Для выхода из чата используйте <b>/exit</b>"
OPERATOR_TICKET_CLOSED = "🔴 Тикет закрыт. Диалог завершён."
USER_OPERATOR_WAIT = "🕐 Ваш <b>запрос передан оператору</b>. Ожидайте, он скоро подключится."
USER_OPERATOR_CONNECTED = "✅ Оператор подключился. Ожидайте, уже ознакамливаемся с вопросом."
USER_OPERATOR_CLOSED = "🔴 Диалог с оператором <b>завершён</b>."


def operator_new_ticket(ticket_id: int, username: str, dialog_type: str | None, query: str) -> str:
    return (
        f"🔔 <b>Новый тикет №{ticket_id}</b>\n\n"
        f"👤 Пользователь: <i>{username}</i>\n"
        f"📂 Тип: <code>{dialog_type or 'неизвестно'}</code>\n\n"
        f"💬 Запрос:\n{query}"
    )


def operator_ticket_accepted(ticket_id: int) -> str:
    return f"✅ Вы приняли <b>тикет #{ticket_id}</b>\n/close - завершить диалог."
