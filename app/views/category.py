from app.schemas.category import ResponseCategory, CreateCategory, UpdateCategory
from fastapi import APIRouter, Depends, Body, HTTPException, status, Query, Path
from app.crud import category
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.db_helper import db_helper

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
):
    new_category = await category.create_category_crud(
        category_data=category_data, session=session
    )
    if new_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Передан не существующий пользователь для создания категории",
        )
    return new_category


@router.get("/", response_model=list[ResponseCategory])
async def get_list_category(
    start: int = Query(0, description="Начало диапазона для поиска"),
    stop: int = Query(3, description="Конец диапазона для поиска"),
    session: AsyncSession = Depends(db_helper.get_session),
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


@router.get("/{category_id}", response_model=ResponseCategory)
async def get_category_by_id(
    category_id: Annotated[int, Path(ge=1, description="ID категории для поиска")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    current_category = await category.get_category_by_id_crud(
        category_id=category_id,
        session=session,
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
):
    update_category = await category.update_category_crud(
        category_data=category_data, category_id=category_id, session=session
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
):
    delete_category = await category.delete_category_crud(
        category_id=category_id, session=session
    )
    if delete_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    return delete_category
