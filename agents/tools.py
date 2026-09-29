from langchain.tools import tool
from app.crud.user import get_top_spending_by_category_crud, get_total_sum_by_day_crud
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
        print("TOOL ВЫЗВАН, функция считающая топ трат с группировкой по категориям")
        # print("Вызвана", get_top_spending_by_category_tools.__name__)
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
        date_from: date | None = None,
        date_to: date | None = None,
        limit: int = 3,
        order: str = "asc",
    ):
        """
        Возвращает список транзакций(трат) пользователя.

        amount — количество купленных единиц.
        cost — цена одной единицы.
        total_cost — итоговая стоимость всей транзакции: amount * cost.

        При ответе пользователю для суммы конкретной траты всегда используй total_cost.
        Никогда не используй cost как общую сумму покупки.
        Не вычисляй total_cost самостоятельно, используй значение из результата инструмента.

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

        print("Выводим список транзакций!!")
        # print("date_from", date_from)
        # print("date_to", date_to)

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
                    "total_cost": transaction.amount * transaction.cost,
                }
            )
        return response

    @tool
    async def get_total_sum_by_day_tools(
        date_from: date,
        date_to: date,
    ):
        """
        Функция возвращает общую сумму затрат пользователя с группировкой по дням.
        Ответ приходит в виде списка кортежей. Где на первой позиции значение суммы -
        используй его для вывода общих затрат за день. И 2 значение это дата, в формате 2025-07-04 (гг-мм-дд)
        Args:
            date_from : Начальная дата периода
            date_to: Конечная дата периода
        """

        print("Считаем и выводим суммы по дням")
        total_days_sum: list[tuple] = await get_total_sum_by_day_crud(
            session=session,
            user_db=user_db,
            date_from=date_from,
            date_to=date_to,
        )
        print(total_days_sum)
        return total_days_sum

    return [
        get_list_transactions_tools,
        get_top_spending_by_category_tools,
        get_total_sum_by_day_tools,
    ]
