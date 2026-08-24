from fastapi import APIRouter, Depends, Body, HTTPException, status
from app.db.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.transaction import CreateTransaction, ResponseTransaction
from typing import Annotated
from app.crud import transaction
from app.exc.error import (
    UserSearchError,
    CategorySearchError,
    DateError,
    TransactionCreateError,
)

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
):
    try:
        new_transaction = await transaction.create_transaction_crud(
            transaction_data=transaction_data, session=session
        )
    except UserSearchError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    except CategorySearchError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    except DateError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Указана не корректная дата"
        )
    except TransactionCreateError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У пользователя нет такой категории затрат",
        )
    return new_transaction
