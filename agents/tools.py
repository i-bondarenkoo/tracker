from langchain.tools import tool


@tool
def get_my_id() -> int:
    """
    Возвращает ID текущего пользователя.
    """
    return 123


tools = [get_my_id]
