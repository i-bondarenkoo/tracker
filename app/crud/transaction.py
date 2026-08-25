from app.schemas.transaction import CreateTransaction, UpdateTransaction
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user
from app.crud import category
from app.exc.error import (
    UserSearchError,
    CategorySearchError,
    DateError,
    TransactionCreateError,
)
from app.models.transaction import Transaction
from datetime import date
from sqlalchemy import select


async def create_transaction_crud(
    transaction_data: CreateTransaction, session: AsyncSession
):
    current_user = await user.get_user_by_id_crud(
        user_id=transaction_data.user_id, session=session
    )
    if current_user is None:
        raise UserSearchError
    current_category = await category.get_category_by_id_crud(
        category_id=transaction_data.category_id, session=session
    )
    if current_category is None:
        raise CategorySearchError
    if (
        current_category.user_id != transaction_data.user_id
        and current_category.user_id is not None
    ):
        raise TransactionCreateError
    current_date = date.today()
    if transaction_data.transaction_date > current_date:
        raise DateError
    new_transaction = Transaction(**transaction_data.model_dump())
    session.add(new_transaction)
    await session.commit()
    await session.refresh(new_transaction)
    return new_transaction


async def get_transaction_by_id_crud(
    transaction_id: int,
    session: AsyncSession,
):
    current_transaction = await session.get(Transaction, transaction_id)
    return current_transaction


async def get_list_transactions_crud(
    session: AsyncSession,
    start: int = 0,
    stop: int = 3,
):
    stmt = (
        select(Transaction).order_by(Transaction.id).limit(stop - start).offset(start)
    )
    result = await session.execute(stmt)
    transactions: list = result.scalars().all()
    return transactions


async def update_transaction_crud(
    transaction_data: UpdateTransaction,
    transaction_id: int,
    session: AsyncSession,
):
    update_transaction = await get_transaction_by_id_crud(
        transaction_id=transaction_id, session=session
    )
    if update_transaction is None:
        return None
    current_date = date.today()
    if (
        transaction_data.transaction_date
        and transaction_data.transaction_date > current_date
    ):
        raise DateError
    update_data: dict = transaction_data.model_dump(exclude_unset=True)
    if len(update_data) == 0:
        return update_transaction
    for k, v in update_data.items():
        setattr(update_transaction, k, v)
    await session.commit()
    await session.refresh(update_transaction)
    return update_transaction
