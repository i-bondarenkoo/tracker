from email.policy import HTTP

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.db_helper import db_helper
from fastapi import Depends, Body, APIRouter, HTTPException, Query, status, Path
from app.schemas.user import CreateUser, ResponseUser, UpdateUserPatch, UpdateUserFull
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


@router.get("/{user_id}", response_model=ResponseUser)
async def get_user_by_id(
    user_id: Annotated[
        int, Path(ge=1, description="ID пользователя для получения данных")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):
    current_user = await user.get_user_by_id_crud(user_id=user_id, session=session)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return current_user


@router.get("/", response_model=list[ResponseUser])
async def get_list_users(
    start: int = Query(0, ge=0, description="Начальный диапазон"),
    stop: int = Query(3, gt=1, description="Конечный диапазон"),
    session: AsyncSession = Depends(db_helper.get_session),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Задан не корректный диапазон",
        )
    users = await user.get_list_users_crud(start=start, stop=stop, session=session)
    return users


@router.patch("/{user_id}", response_model=ResponseUser)
async def update_user_partial(
    user_id: Annotated[
        int, Path(ge=1, description="ID пользователя для обновления данных")
    ],
    user_data: Annotated[UpdateUserPatch, Body(description="Данные для обновления")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    try:
        update_user = await user.update_user_crud(
            user_id=user_id,
            session=session,
            user_data=user_data,
            partial=True,
        )
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой почтой уже существует",
        )
    if update_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return update_user


@router.put("/{user_id}", response_model=ResponseUser)
async def update_user(
    user_id: Annotated[
        int, Path(ge=1, description="ID пользователя для обновления данных")
    ],
    user_data: Annotated[UpdateUserFull, Body(description="Данные для обновления")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    try:
        update_user = await user.update_user_crud(
            user_id=user_id,
            session=session,
            user_data=user_data,
            partial=False,
        )
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой почтой уже существует",
        )
    if update_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return update_user
