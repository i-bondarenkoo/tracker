from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.db_helper import db_helper
from fastapi import Depends, Body, APIRouter, HTTPException, Query, status, Path
from app.schemas.user import (
    ResponseUserExtended,
    ResponseUser,
    UpdateUserPatch,
    UpdateUserFull,
    ResponseUserCost,
    ResponseUserTopCost,
    ResponseUserAvgValue,
)
from app.crud import user
from app.exc.error import DateError
from sqlalchemy.exc import IntegrityError
from datetime import date
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # dependencies=[Depends(get_current_user)],
)


@router.get("/me", response_model=ResponseUserExtended)
async def get_user_by_id(
    session: AsyncSession = Depends(db_helper.get_session),
    query_parametrs: str = Query(
        "",
        description="Параметр для подгрузки связанных с пользователем объектов. Пример ввода, строкой через , (categories, transactions)",
    ),
    user_db: User = Depends(get_current_user),
):

    current_user = await user.get_user_by_id_extended_crud(
        user_db=user_db,
        session=session,
        query_parametrs=query_parametrs,
    )
    return current_user


@router.get("/", response_model=list[ResponseUser])
async def get_list_users(
    start: int = Query(0, ge=0, description="Начальный диапазон"),
    stop: int = Query(3, gt=1, description="Конечный диапазон"),
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Задан не корректный диапазон",
        )
    users = await user.get_list_users_crud(start=start, stop=stop, session=session)
    return users


@router.patch("/me", response_model=ResponseUser)
async def update_user_partial(
    user_data: Annotated[UpdateUserPatch, Body(description="Данные для обновления")],
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    try:
        update_user = await user.update_user_crud(
            user_db=user_db,
            session=session,
            user_data=user_data,
            partial=True,
        )
    except IntegrityError as e:
        print(e)
        await session.rollback()
        if "email" in str(e.orig):
            raise HTTPException(
                status_code=409, detail="Пользователь с такой почтой уже существует"
            )
        raise HTTPException(
            status_code=400, detail="Некорректные данные для обновления"
        )
    return update_user


@router.put("/me", response_model=ResponseUser)
async def update_user(
    user_data: Annotated[UpdateUserFull, Body(description="Данные для обновления")],
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    try:
        update_user = await user.update_user_crud(
            user_db=user_db,
            session=session,
            user_data=user_data,
            partial=False,
        )
    except IntegrityError as e:
        await session.rollback()
        if "email" in str(e.orig):
            raise HTTPException(
                status_code=409, detail="Пользователь с такой почтой уже существует"
            )
        raise HTTPException(
            status_code=400, detail="Некорректные данные для обновления"
        )
    return update_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_db: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.get_session),
):
    delete_user = await user.delete_user_crud(user_db=user_db, session=session)
    return delete_user


@router.get("/me/spending-by-category", response_model=list[ResponseUserCost])
async def get_speding_by_category(
    session: AsyncSession = Depends(db_helper.get_session),
    date_from: date = Query(description="Начальная дата поиска"),
    date_to: date = Query(description="Конечная дата поиска"),
    user_db: User = Depends(get_current_user),
):
    try:
        total = await user.get_spending_by_category_crud(
            user_db=user_db, session=session, date_to=date_to, date_from=date_from
        )
    except DateError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный диапазон даты",
        )
    return total


@router.get("/me/spending-top-categories", response_model=list[ResponseUserTopCost])
async def get_top_spending_by_category(
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
    date_from: date = Query(),
    date_to: date = Query(),
    limit: int = Query(3, ge=1),
):
    try:
        total = await user.get_top_spending_by_category_crud(
            user_db=user_db,
            session=session,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
        )
    except DateError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный диапазон даты",
        )
    return total


@router.get("/me/transactions-average-value", response_model=list[ResponseUserAvgValue])
async def get_transactions_average_value(
    date_from: date = Query(),
    date_to: date = Query(),
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    try:
        total = await user.get_transactions_average_value_crud(
            user_db=user_db,
            session=session,
            date_from=date_from,
            date_to=date_to,
        )
    except DateError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный диапазон даты",
        )
    return total
