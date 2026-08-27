from pydantic import EmailStr

from app.crud.helper import build_response
from app.schemas.user import CreateUser, UpdateUserPatch, UpdateUserFull
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload, joinedload


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
