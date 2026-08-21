from pydantic import EmailStr

from app.schemas.user import CreateUser
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
