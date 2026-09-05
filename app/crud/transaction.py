from app.schemas.transaction import CreateTransaction, UpdateTransaction
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user
from app.crud import category
from app.exc.error import (
    CategorySearchError,
    DateError,
    TransactionCreateError,
    GetTransactionError,
)
from sqlalchemy import Result
from app.models.transaction import Transaction
from datetime import date
from app.models.user import User
from sqlalchemy import select


async def create_transaction_crud(
    transaction_data: CreateTransaction,
    session: AsyncSession,
    user_db: User,
):

    current_category = await category.get_category_by_id_crud(
        category_id=transaction_data.category_id, session=session
    )
    if current_category is None:
        raise CategorySearchError
    if current_category.user_id != user_db.id and current_category.user_id is not None:
        raise TransactionCreateError
    current_date = date.today()
    if transaction_data.transaction_date > current_date:
        raise DateError
    new_transaction = Transaction(
        amount=transaction_data.amount,
        cost=transaction_data.cost,
        category_id=transaction_data.category_id,
        user_id=user_db.id,
        description=transaction_data.description,
        transaction_date=transaction_data.transaction_date,
    )
    session.add(new_transaction)
    await session.commit()
    await session.refresh(new_transaction)
    return new_transaction


async def get_transaction_by_id_crud(
    transaction_id: int,
    session: AsyncSession,
    user_db: User,
):
    stmt = (
        select(Transaction)
        .filter(Transaction.id == transaction_id)
        .order_by(Transaction.id)
    )
    result: Result = await session.execute(stmt)
    transations: Transaction = result.scalars().one_or_none()
    if transations is None:
        return None
    if transations.user_id != user_db.id:
        raise GetTransactionError
    return transations


async def get_list_transactions_crud(
    user_db: User,
    session: AsyncSession,
    start: int = 0,
    stop: int = 3,
):
    stmt = (
        select(Transaction)
        .filter(Transaction.user_id == user_db.id)
        .order_by(Transaction.id)
        .limit(stop - start)
        .offset(start)
    )
    result = await session.execute(stmt)
    transactions: list = result.scalars().all()
    return transactions


async def update_transaction_crud(
    transaction_data: UpdateTransaction,
    transaction_id: int,
    session: AsyncSession,
    user_db: User,
):
    update_transaction = await get_transaction_by_id_crud(
        transaction_id=transaction_id,
        session=session,
        user_db=user_db,
    )
    if update_transaction is None:
        return None
    current_date = date.today()
    if (
        transaction_data.transaction_date
        and transaction_data.transaction_date > current_date
    ):
        raise DateError
    if user_db.id != update_transaction.user_id:
        raise GetTransactionError
    update_data: dict = transaction_data.model_dump(exclude_unset=True)
    if len(update_data) == 0:
        return update_transaction
    for k, v in update_data.items():
        setattr(update_transaction, k, v)
    await session.commit()
    await session.refresh(update_transaction)
    return update_transaction


async def delete_transaction_crud(
    transaction_id: int,
    session: AsyncSession,
    user_db: User,
):
    delete_transaction = await get_transaction_by_id_crud(
        transaction_id=transaction_id, session=session, user_db=user_db
    )
    if delete_transaction is None:
        return None
    if user_db.id != delete_transaction.user_id:
        raise GetTransactionError
    await session.delete(delete_transaction)
    await session.commit()
    return {"message": "delete"}
