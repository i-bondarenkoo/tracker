from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.schemas.user import ResponseUser, CreateUser
from app.models.user import User
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_helper import db_helper
from app.crud import user
from sqlalchemy.exc import IntegrityError
from app.schemas.token import ResponseToken
from app.auth.dependencies import user_auth, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register",
    response_model=ResponseUser,
    status_code=status.HTTP_201_CREATED,
)
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


@router.post("/login", response_model=ResponseToken)
async def login(current_user: User = Depends(user_auth)):

    token = create_access_token(current_user=current_user)
    return ResponseToken(
        access_token=token,
    )
