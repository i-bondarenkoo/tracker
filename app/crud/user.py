from pydantic import EmailStr

from app.schemas.user import CreateUser, UpdateUserPatch, UpdateUserFull
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select, Result


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


async def get_user_by_id_crud(user_id: int, session: AsyncSession):
    current_user = await session.get(User, user_id)
    return current_user


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
