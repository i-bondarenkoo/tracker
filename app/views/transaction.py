from fastapi import APIRouter, Depends, Body, HTTPException, status, Path, Query
from app.db.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.transaction import (
    CreateTransaction,
    ResponseTransaction,
    UpdateTransaction,
)
from typing import Annotated
from app.crud import transaction
from app.exc.error import (
    CategorySearchError,
    DateError,
    TransactionCreateError,
    GetTransactionError,
)
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"],
)


@router.post(
    "/", response_model=ResponseTransaction, status_code=status.HTTP_201_CREATED
)
async def create_transaction(
    transaction_data: Annotated[CreateTransaction, Body()],
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    try:
        new_transaction = await transaction.create_transaction_crud(
            transaction_data=transaction_data,
            session=session,
            user_db=user_db,
        )
    except CategorySearchError:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    except TransactionCreateError:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У пользователя нет такой категории затрат",
        )
    except DateError:
        # await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Указана не корректная дата"
        )
    return new_transaction


@router.get("/{transaction_id}", response_model=ResponseTransaction)
async def get_transaction_by_id(
    transaction_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    try:
        current_transaction = await transaction.get_transaction_by_id_crud(
            transaction_id=transaction_id,
            session=session,
            user_db=user_db,
        )
    except GetTransactionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя посмотреть данные чужой транзакции",
        )
    if current_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Транзакции(затрата) не найдены",
        )
    return current_transaction


@router.get("/", response_model=list[ResponseTransaction])
async def get_list_transactions(
    user_db: User = Depends(get_current_user),
    start: int = Query(0, ge=0),
    stop: int = Query(3, gt=1),
    session: AsyncSession = Depends(db_helper.get_session),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Задан не корректный диапазон",
        )
    transactions: list = await transaction.get_list_transactions_crud(
        start=start,
        user_db=user_db,
        stop=stop,
        session=session,
    )
    return transactions


@router.patch("/{transaction_id}", response_model=ResponseTransaction)
async def update_transaction(
    transaction_id: Annotated[int, Path(ge=1)],
    transaction_data: Annotated[UpdateTransaction, Body()],
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    try:
        update_transaction = await transaction.update_transaction_crud(
            transaction_id=transaction_id,
            session=session,
            user_db=user_db,
            transaction_data=transaction_data,
        )
    except DateError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Указана не корректная дата"
        )
    except GetTransactionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя обновить данные чужой транзакции",
        )
    if update_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Транзакция(затрата) не найдена",
        )
    return update_transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.get_session),
    user_db: User = Depends(get_current_user),
):
    try:
        delete_transaction = await transaction.delete_transaction_crud(
            transaction_id=transaction_id,
            session=session,
            user_db=user_db,
        )
    except GetTransactionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя удалить данные чужой транзакции",
        )
    if delete_transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Транзакция(затрата) не найдена",
        )
    return delete_transaction
