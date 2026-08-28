from pydantic import EmailStr

from app.crud.helper import (
    build_response,
    build_response_user_cost,
)
from app.schemas import user
from app.schemas.user import CreateUser, UpdateUserPatch, UpdateUserFull
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload, joinedload
from datetime import date
from app.exc.error import DateError
from sqlalchemy import func
from app.models.transaction import Transaction
from app.models.category import Category


async def create_user_crud(user_data: CreateUser, session: AsyncSession):

    new_user = User(**user_data.model_dump())
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
    user_id: int,
    session: AsyncSession,
    query_parametrs: str,
):
    params: set = {"categories", "transactions"}
    for_query: list = []
    if len(query_parametrs) == 0:
        current_user = await session.get(User, user_id)
        if current_user is None:
            return None
        return build_response(current_object=current_user, requested=set())
    query_parametrs = [el.strip().lower() for el in query_parametrs.split(",")]
    params_in = set(query_parametrs) & params
    for_query = [selectinload(getattr(User, el)) for el in params_in]
    stmt = select(User).where(User.id == user_id).options(*for_query)
    result = await session.execute(stmt)
    user: User = result.scalars().one_or_none()
    if user is None:
        return None
    response = build_response(current_object=user, requested=params_in)
    return response


async def get_list_users_crud(session: AsyncSession, start: int = 1, stop: int = 3):
    stmt = select(User).order_by(User.id).limit(stop - start).offset(start)
    result: Result = await session.execute(stmt)
    users: list = result.scalars().all()
    return users


async def update_user_crud(
    user_id: int,
    user_data: UpdateUserPatch | UpdateUserFull,
    session: AsyncSession,
    partial: bool,
):
    update_user = await get_user_by_id_crud(user_id=user_id, session=session)
    if update_user is None:
        return None
    # exclude_unset - добавляем в словарь только те поля, которые передали
    update_data: dict = user_data.model_dump(exclude_unset=partial)
    if len(update_data) == 0:
        return update_user
    for k, v in update_data.items():
        # if v is not None:
        setattr(update_user, k, v)
    await session.commit()
    await session.refresh(update_user)
    return update_user


async def delete_user_crud(
    user_id: int,
    session: AsyncSession,
) -> None:
    delete_user = await get_user_by_id_crud(user_id=user_id, session=session)
    if delete_user is None:
        return None
    await session.delete(delete_user)
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
    user_id: int,
    session: AsyncSession,
    date_from: date,
    date_to: date,
):
    if date_from > date_to:
        raise DateError
    current_user = await get_user_by_id_crud(user_id=user_id, session=session)
    if current_user is None:
        return None
    stmt = (
        select(
            Transaction.category_id,
            func.sum(Transaction.amount * Transaction.cost).label(
                "total_amount_by_category"
            ),
        )
        .filter(
            Transaction.user_id == user_id,
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
    user_id: int,
    session: AsyncSession,
    date_from: date,
    date_to: date,
    limit: int = 3,
):
    if date_from > date_to:
        raise DateError
    current_user = await get_user_by_id_crud(user_id=user_id, session=session)
    if current_user is None:
        return None
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
            Transaction.user_id == user_id,
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


# Вывести траты/транзакции пользователя с именем и фамилией
# которые больше среднего чека этого пользователя
# за период времени
async def get_transactions_average_value_crud(
    user_id: int,
    date_from: date,
    date_to: date,
    session: AsyncSession,
):
    if date_from > date_to:
        raise DateError
    current_user = await get_user_by_id_crud(user_id=user_id, session=session)
    if current_user is None:
        return None
    query = (
        select(func.avg(Transaction.amount * Transaction.cost).label("avg"))
        .filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date.between(date_from, date_to),
        )
        .scalar_subquery()
    )
    stmt = select(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_date.between(date_from, date_to),
        Transaction.amount * Transaction.cost > query,
    )

    result = await session.execute(stmt)
    total = result.scalars().all()
    print(total)
    return total
