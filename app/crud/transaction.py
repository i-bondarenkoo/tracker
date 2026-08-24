from app.schemas.transaction import CreateTransaction
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


async def create_transaction_crud(
    transaction_data: CreateTransaction, session: AsyncSession
):
    check_user = await user.get_user_by_id_crud(
        user_id=transaction_data.user_id, session=session
    )
    if check_user is None:
        raise UserSearchError
    check_category = await category.get_category_by_id_crud(
        category_id=transaction_data.category_id, session=session
    )
    if check_category is None:
        raise CategorySearchError
    if (
        check_category.user_id != transaction_data.user_id
        and check_category.user_id is not None
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
