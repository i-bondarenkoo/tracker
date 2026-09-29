from langchain.tools import tool
from app.crud.user import get_top_spending_by_category_crud
from datetime import date
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.transaction import get_list_transactions_crud
from app.schemas.transaction import ResponseTransaction
from agents.services import get_all_category


def create_tools(
    user_db: User,
    session: AsyncSession,
):
    @tool
    async def get_top_spending_by_category_tools(
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
    async def get_list_transactions_tools(
        date_from: date,
        date_to: date,
        limit: int = 3,
        order: str = "asc",
    ):
        """
        Возвращает список транзакций(трат) пользователя.
        Сортировка по возрастанию - asc
        Args:
            date_to | None = None: Конечная дата периода .
            date_from | None = None: Начальная дата периода .
            Эти даты могут быть не указаны, и тогда рассматриваем все транзакции
            за все время,
            либо может быть указана одна из границ диапазона
            limit - количество затрат в ответе. Если пользователь не указывает значение,
            использую то, что по умолчанию
            order - тип сортировки, если пользователь просит "последние N затрат" то использовать
            order='desc', если просит "первые N трат" или не указывает ничего - order='asc'
        """

        # print("2 функций для вывода транзакиций")
        # print("date_from", date_from)
        # print("date_to", date_to)
        # print("start", start)
        # print("stop", stop)

        transactions: list[ResponseTransaction] = await get_list_transactions_crud(
            date_from=date_from,
            date_to=date_to,
            session=session,
            limit=limit,
            order=order,
            user_db=user_db,
        )
        # print("Resultat", result)
        response = []
        category_ids: list[int] = [
            transaction.category_id for transaction in transactions
        ]
        categories = await get_all_category(category_ids=category_ids, session=session)
        categories_by_id: dict = {category.id: category.name for category in categories}
        for transaction in transactions:
            response.append(
                {
                    "id": transaction.id,
                    "amount": transaction.amount,
                    "cost": transaction.cost,
                    "description": transaction.description,
                    "transaction_date": transaction.transaction_date,
                    "category": categories_by_id[transaction.category_id],
                }
            )
        return response

    return [get_list_transactions_tools, get_top_spending_by_category_tools]
