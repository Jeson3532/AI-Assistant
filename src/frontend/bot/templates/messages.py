START_MESSAGE = "👋 Привет! Я <b>ассистент Рецифры</b> для оперативного решения задач в digital-агенстве.\nВыбери то, что тебя интересует:"
ASSISTANT_START_MESSAGE = "🤖 | Вы перешли в чат с нейросетевым ассистентом.\nЗадайте интересующий Вас вопрос и получите на него ответ. Для выхода из чата используйте <b>/exit</b>"
OPERATOR_TICKET_CLOSED = "🔴 | Тикет закрыт. Диалог завершён."
USER_OPERATOR_WAIT = "🕐 | Ваш <b>запрос передан оператору</b>. Ожидайте, он скоро подключится."
USER_OPERATOR_CONNECTED = "✅ | <b>Оператор подключился</b>. Ожидайте, уже ознакамливаемся с вопросом."
USER_OPERATOR_CLOSED = "🔴 | Диалог с оператором <b>завершён</b>."
DIALOG_TYPE_LABELS = {
    "task_status": "Статус задачи",
    "technical_error": "Техническая ошибка",
    "content_edit": "Контентная правка",
    "access": "Доступы",
    "integration": "Интеграция",
    "analytics": "Аналитика",
    "organizational": "Орг. вопросы",
    "urgent": "Срочное",
    "small_talk": "Неформально",
    "other": "Прочее",
}
APP_INFO_MESSAGE = """
🧩 <b>ИИ-АССИСТЕНТ В "РЕЦИФРА"</b>\n\n
Интеллектуальный помощник в <b>digital-агенстве</b> поможет Вашей компании оперативно решать задачи без затрат на штаб операторов разных направлений.\n
<b>Ключевая идея</b> - создать интеллектуального помощника, который использует внутреннюю базу знаний для поиска уже решенных вопросов с целью сократить время на поиск информации для сотрудников компании.
\n
🤟 Начало в три шага:
<i>1. Запусти бота
2. Задай свой вопрос нейро-ассистенту
3. Получи ответ в кратчайшие сроки</i>
\n
---
<b>👨‍💼 Разработчик:</b> <a href="https://github.com/Jeson3532">Jeson</a>
<b>🕑 Дата окончания разработки:</b> 17.05.2026
<b>🌗 Версия продукта:</b> MVP
"""


def operator_new_ticket(ticket_id: int, username: str, dialog_type: str | None, query: str) -> str:
    return (
        f"🔔 <b>Новый тикет №{ticket_id}</b>\n\n"
        f"👤 Пользователь: <i>{username}</i>\n"
        f"📂 Тип: <code>{dialog_type or 'неизвестно'}</code>\n\n"
        f"💬 Запрос:\n{query}"
    )


def operator_ticket_accepted(ticket_id: int) -> str:
    return f"✅ Вы приняли <b>тикет #{ticket_id}</b>\n/close - завершить диалог."


def format_analytics(data: dict) -> str:
    total = data["total"]
    auto = data["auto_handled"]
    op = data["operator_handled"]
    auto_pct = round(auto / total * 100) if total else 0
    op_pct = round(op / total * 100) if total else 0

    by_type_lines = "\n".join([
        f"  • {DIALOG_TYPE_LABELS.get(row['dialog_type'], row['dialog_type'] or 'неизвестно')}: <b>{row['count']}</b>"
        for row in data["by_type"]
    ])

    return (
        f"📊 <b>Статистика ассистента</b>\n\n"
        f"📨 Всего обращений: <b>{total}</b>\n"
        f"🤖 Авто-ответов: <b>{auto}</b> ({auto_pct}%)\n"
        f"👨‍💼 Передано оператору: <b>{op}</b> ({op_pct}%)\n\n"
        f"📂 <b>По типам:</b>\n{by_type_lines}"
    )


def format_journal(data: dict) -> str:
    items = data["items"]
    total = data["total"]
    if not items:
        return "📋 Журнал пуст."

    lines = []
    for item in items:
        dtype = DIALOG_TYPE_LABELS.get(item.get("dialog_type"), item.get("dialog_type") or "—")
        op_mark = "👨‍💼" if item["operator"] else "🤖"
        date = item["finished_at"][:10]
        history = item.get("history") or []
        first_msg = next(
            (m["text"] for m in history if isinstance(m, dict) and m.get("role") == "user"),
            "-"
        )
        short = first_msg[:5] + "..." if len(first_msg) > 60 else first_msg
        lines.append(f"{op_mark} <code>{date}</code> [{dtype}]\n    <i>{short}</i>")

    body = "\n\n".join(lines)
    return f"📋 <b>Последние обращения</b> (всего {total}):\n\n{body}"
