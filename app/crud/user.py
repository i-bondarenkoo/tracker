from pydantic import EmailStr
import asyncio
from app.crud.helper import (
    build_response_percentage_user_transactions,
    build_response_user,
    build_response_user_cost,
    build_response_comparison,
    calculate_percentage_difference_by_month,
    get_date_helper,
)
from app.schemas.user import (
    CreateUser,
    UpdateUserPatch,
    UpdateUserFull,
    ResponseComparisonTransactionByMonth,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload, joinedload
from datetime import date
from app.exc.error import DateError
from sqlalchemy import func
from app.models.transaction import Transaction
from app.models.category import Category
from app.auth.service import hash_password
from app.crud import category
import calendar


async def create_user_crud(user_data: CreateUser, session: AsyncSession):

    new_user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        password_hash=hash_password(password=user_data.password),
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_email_crud(email: EmailStr, session: AsyncSession):
    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    return user


async def get_user_by_id_crud(
    user_id: int,
    session: AsyncSession,
):
    user = await session.get(User, user_id)
    return user


async def get_user_by_id_extended_crud(
    user_db: User,
    session: AsyncSession,
    query_parametrs: str,
):
    params: set = {"categories", "transactions"}
    for_query: list = []
    if len(query_parametrs) == 0:
        return build_response_user(current_object=user_db, requested=set())

    query_parametrs = [el.strip().lower() for el in query_parametrs.split(",")]
    params_in = set(query_parametrs) & params
    for_query = [selectinload(getattr(User, el)) for el in params_in]
    stmt = select(User).where(User.id == user_db.id).options(*for_query)
    result = await session.execute(stmt)
    user_with_relations: User = result.scalars().one_or_none()
    response = build_response_user(
        current_object=user_with_relations, requested=params_in
    )
    return response


async def get_list_users_crud(session: AsyncSession, start: int = 1, stop: int = 3):
    stmt = select(User).order_by(User.id).limit(stop - start).offset(start)
    result: Result = await session.execute(stmt)
    users: list = result.scalars().all()
    return users


async def update_user_crud(
    user_db: User,
    user_data: UpdateUserPatch | UpdateUserFull,
    session: AsyncSession,
    partial: bool,
):

    # exclude_unset - добавляем в словарь только те поля, которые передали
    update_data: dict = user_data.model_dump(exclude_unset=partial)
    if len(update_data) == 0:
        return user_db
    for k, v in update_data.items():
        # if v is not None:
        setattr(user_db, k, v)
    await session.commit()
    await session.refresh(user_db)
    return user_db


async def delete_user_crud(
    user_db: User,
    session: AsyncSession,
) -> None:
    await session.delete(user_db)
    await session.commit()
    return {"message": "delete"}


# 1-n relation
# async def get_user_with_categories_crud(
#     user_id: int,
#     session: AsyncSession,
# ):
#     stmt = (
#         select(User)
#         .where(User.id == user_id)
#         .options(
#             selectinload(
#                 User.categories,
#             )
#         )
#     )
#     result = await session.execute(stmt)
#     current_user = result.scalars().one_or_none()
#     return current_user


# Посчитать сумму трат по категориям
# за период времени для пользователя
async def get_spending_by_category_crud(
    user_db: User,
    session: AsyncSession,
    date_from: date,
    date_to: date,
):
    if date_from > date_to:
        raise DateError
    stmt = (
        select(
            Transaction.category_id,
            func.sum(Transaction.amount * Transaction.cost).label(
                "total_amount_by_category"
            ),
        )
        .filter(
            Transaction.user_id == user_db.id,
            Transaction.transaction_date.between(date_from, date_to),
        )
        .group_by(Transaction.category_id)
    )
    result: Result = await session.execute(stmt)
    print(result)
    total_amount: list[tuple] = result.all()
    print(total_amount)
    return build_response_user_cost(data_in=total_amount)
    # return total_amount


# Топ 3 категории по тратам за период
async def get_top_spending_by_category_crud(
    user_db: User,
    session: AsyncSession,
    date_from: date,
    date_to: date,
    limit: int = 3,
):
    if date_from > date_to:
        raise DateError
    stmt = (
        select(
            Category.name,
            Transaction.category_id,
            func.sum(Transaction.amount * Transaction.cost).label(
                "total_amount_by_category"
            ),
        )
        .join(Category)
        .filter(
            Transaction.user_id == user_db.id,
            # Category.id == Transaction.category_id,
            Transaction.transaction_date.between(date_from, date_to),
        )
        .group_by(Transaction.category_id, Category.name)
        .order_by(func.sum(Transaction.amount * Transaction.cost).desc())
        .limit(limit)
    )
    result: Result = await session.execute(stmt)
    total_amount = result.all()
    print(total_amount)
    return total_amount


# Вывести траты/транзакции пользователя
# которые больше среднего чека этого пользователя
# за период времени
async def get_transactions_average_value_crud(
    user_db: User,
    date_from: date,
    date_to: date,
    session: AsyncSession,
):
    if date_from > date_to:
        raise DateError

    query = (
        select(func.avg(Transaction.amount * Transaction.cost).label("avg"))
        .filter(
            Transaction.user_id == user_db.id,
            Transaction.transaction_date.between(date_from, date_to),
        )
        .scalar_subquery()
    )
    stmt = select(Transaction).filter(
        Transaction.user_id == user_db.id,
        Transaction.transaction_date.between(date_from, date_to),
        Transaction.amount * Transaction.cost > query,
    )

    result = await session.execute(stmt)
    total = result.scalars().all()
    print(total)
    return total


# Посчитать процент трат по каждой категории от общей суммы
# за определенный период времени
async def get_precentage_from_total_amount_crud(
    session: AsyncSession,
    user_db: User,
    date_from: date | None = None,
    date_to: date | None = None,
):
    filter_date: list = [Transaction.user_id == user_db.id]
    if date_from is not None and date_to is not None:
        filter_date.append(Transaction.transaction_date.between(date_from, date_to))
    elif date_from is not None:
        filter_date.append(Transaction.transaction_date >= date_from)
    elif date_to is not None:
        filter_date.append(Transaction.transaction_date <= date_to)
    query = await session.execute(
        (
            select(
                Transaction.category_id,
                func.sum(Transaction.cost * Transaction.amount).label(
                    "user_sum_by_category"
                ),
            )
            .filter(*filter_date)
            .group_by(Transaction.category_id)
        )
    )
    query_2 = await session.execute(
        select(func.sum(Transaction.amount * Transaction.cost)).filter(*filter_date)
    )
    sum_by_category: list[tuple] = query.all()
    print("sum_by_category", sum_by_category)
    total_sum = query_2.scalars().one_or_none()
    if total_sum is None:
        return None
    print("total_sum", total_sum)
    result = []
    for e in sum_by_category:
        digit = round(e[1] * 100 / total_sum, 2)
        current_category = await category.get_category_by_id_crud(
            session=session, category_id=e[0]
        )
        result.append((current_category.name, digit))
    return build_response_percentage_user_transactions(data_in=result)


# Сравнить траты пользователя по месяцам
# Для каждой категории показать сумму в этом месяце и в том, который он выберет
# и вывести разницу в процентах
async def get_comparison_by_month_crud(
    user_db: User,
    session: AsyncSession,
    previous_month: date,
    current_month: date,
):
    if previous_month > current_month:
        raise DateError
    all_date: dict = get_date_helper(
        prev_month=previous_month, curr_month=current_month
    )
    query_prev_month = (
        select(
            Transaction.category_id,
            func.sum(Transaction.cost * Transaction.amount),
        )
        .filter(
            Transaction.user_id == user_db.id,
            Transaction.transaction_date.between(
                all_date["start_prev_month"], all_date["end_prev_month"]
            ),
        )
        .group_by(Transaction.category_id)
    )
    query_curr_month = (
        select(
            Transaction.category_id,
            func.sum(Transaction.cost * Transaction.amount),
        )
        .filter(
            Transaction.user_id == user_db.id,
            Transaction.transaction_date.between(
                all_date["start_curr_month"], all_date["end_curr_month"]
            ),
        )
        .group_by(Transaction.category_id)
    )
    query_curr_month, query_prev_month = await asyncio.gather(
        session.execute(query_prev_month),
        session.execute(query_curr_month),
    )
    prev_month_data: list[tuple] = query_prev_month.all()
    curr_month_data: list[tuple] = query_curr_month.all()

    result: list[dict] = calculate_percentage_difference_by_month(
        prev_month_data=prev_month_data,
        curr_month_data=curr_month_data,
    )
    category_ids = [item["category_id"] for item in result]
    query_categories = await session.execute(
        select(Category).filter(Category.id.in_(category_ids))
    )
    categories = query_categories.scalars().all()
    category_names = {cat.id: cat.name for cat in categories}
    for item in result:
        item["category_name"] = category_names.get(
            item["category_id"], "Неизвестная категория"
        )
        del item["category_id"]
    return build_response_comparison(result)
