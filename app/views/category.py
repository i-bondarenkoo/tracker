from app.exc.error import GetCategoryForbidden, GetSharedCategoryForbidden
from app.schemas.category import (
    ResponseCategory,
    CreateCategory,
    UpdateCategory,
    ResponseCategoryExtended,
)
from fastapi import APIRouter, Depends, Body, HTTPException, status, Query, Path
from app.crud import category
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.db_helper import db_helper
from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/category",
    tags=["Category"],
)


@router.post("/", response_model=ResponseCategory, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: Annotated[
        CreateCategory, Body(description="Данные для создания категории")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    new_category = await category.create_category_crud(
        category_data=category_data,
        session=session,
        user_db=user_db,
    )
    return new_category


@router.get("/", response_model=list[ResponseCategory])
async def get_list_category(
    start: int = Query(0, description="Начало диапазона для поиска"),
    stop: int = Query(3, description="Конец диапазона для поиска"),
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Задан не корректный диапазон",
        )
    categories = await category.get_list_category_crud(
        start=start,
        stop=stop,
        session=session,
    )
    return categories


@router.get("/{category_id}", response_model=ResponseCategoryExtended)
async def get_category_by_id(
    category_id: Annotated[int, Path(ge=1, description="ID категории для поиска")],
    session: AsyncSession = Depends(db_helper.get_session),
    query_parametrs: str = Query(
        "",
        description='Аргументы для подгрузки связи к категории. Пример ("transactions, ")',
    ),
    user_db: User = Depends(get_current_user),
):
    try:
        current_category = await category.get_category_by_id_extended_crud(
            category_id=category_id,
            session=session,
            user_db=user_db,
            query_parametrs=query_parametrs,
        )
    except GetCategoryForbidden:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Данная категория не принадлежит пользователю и не является общей",
        )
    if current_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    return current_category


@router.put("/{category_id}", response_model=ResponseCategory)
async def update_category(
    category_id: Annotated[int, Path(ge=1, description="ID категории для обновления")],
    category_data: Annotated[UpdateCategory, Body()],
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    try:
        update_category = await category.update_category_crud(
            user_db=user_db,
            category_data=category_data,
            category_id=category_id,
            session=session,
        )
    except GetCategoryForbidden:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Данная категория не принадлежит пользователю",
        )
    except GetSharedCategoryForbidden:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Данная категория общая, ее нельзя изменить",
        )
    if update_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    return update_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: Annotated[int, Path(ge=1, description="ID категории для удаления")],
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    try:
        delete_category = await category.delete_category_crud(
            user_db=user_db, category_id=category_id, session=session
        )
    except GetCategoryForbidden:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Данная категория не принадлежит пользователю",
        )
    except GetSharedCategoryForbidden:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Данная категория общая, ее нельзя удалить",
        )
    if delete_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    return delete_category
