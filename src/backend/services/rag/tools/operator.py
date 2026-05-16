from langchain.tools import tool


def call_operator(
        user_query: str,
        dialog_type: str,
        response: str | None
):
    """Функция для передачи обращения оператору"""

    return "Передано оператору"
