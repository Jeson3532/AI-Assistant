from langchain.tools import tool

@tool
def call_operator(
        user_query: str,
        dialog_type: str,
        response: str
):
    """Функция для передачи обращения оператору"""

    return True