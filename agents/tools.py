from langchain.tools import tool
from app.crud.user import get_top_spending_by_category_crud
from datetime import date
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.transaction import get_list_transactions_crud


def create_tools(
    user_db: User,
    session: AsyncSession,
):
    @tool
    async def get_top_spending_by_category(
        date_from: date,
        date_to: date,
        limit: int = 3,
    ):
        """
        Возвращает категории, на которые пользователь потратил
        больше всего денег за указанный период.

        Args:
            date_from: Начальная дата периода.
            date_to: Конечная дата периода.
            limit: Максимальное количество категорий в результате.
        """
        # print("TOOL ВЫЗВАН")
        # print(date_from, date_to, limit)
        # print(user_db.id)
        result = await get_top_spending_by_category_crud(
            user_db=user_db,
            date_from=date_from,
            date_to=date_to,
            session=session,
            limit=limit,
        )
        # print("Результат КРУДА", result)
        return result

    @tool
    async def get_list_transactions(
        date_from: date,
        date_to: date,
        start: int = 0,
        stop: int = 3,
    ):
        """
        Возвращает список транзакций(трат) пользователя.
        Сортировка по возрастанию - asc
        Args:
            date_to | None = None: Конечная дата периода .
            date_from | None = None: Начальная дата периода .
            Эти даты могут быть не указаны, и тогда рассматриваем все транзакции за все время,
            либо может быть указана одна из границ диапазона
            start | None = None : Начальный сдвиг в таблице
            stop | None = None : Конечный сдвиг (эта граница не учитывается)
            Пример start=3, stop=5 -> пропустить первые 3 строки, взять следующие 2
        """

        print("2 функций для вывода транзакиций")
        print("date_from", date_from)
        print("date_to", date_to)
        print("start", start)
        print("stop", stop)
        result = await get_list_transactions_crud(
            date_from=date_from,
            date_to=date_to,
            session=session,
            start=start,
            stop=stop,
            user_db=user_db,
        )
        print("Resultat", result)
        return result

    return [get_top_spending_by_category, get_list_transactions]
