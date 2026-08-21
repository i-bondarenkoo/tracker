from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.db_helper import db_helper
from fastapi import Depends, Body, APIRouter, HTTPException, status
from app.schemas.user import CreateUser, ResponseUser
from app.crud import user
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=ResponseUser)
async def create_user(
    user_data: Annotated[
        CreateUser, Body(description="Данные пользователя для создания")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):
    check_user = await user.get_user_by_email_crud(
        email=user_data.email, session=session
    )
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой почтой уже существует",
        )
    try:
        new_user = await user.create_user_crud(user_data=user_data, session=session)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой почтой уже существует",
        )
    return new_user
