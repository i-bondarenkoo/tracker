from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.schemas.category import CreateCategory, UpdateCategory
from app.models.category import Category
from app.crud import user
from sqlalchemy import select
from app.crud.helper import build_response_category
from app.models.user import User
from app.exc.error import GetCategoryForbidden, GetSharedCategoryForbidden
from app.models.transaction import Transaction


async def create_category_crud(
    user_db: User, category_data: CreateCategory, session: AsyncSession
):
    user_id = None if category_data.is_shared else user_db.id
    new_category = Category(name=category_data.name, user_id=user_id)
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category


async def get_category_by_id_crud(category_id: int, session: AsyncSession):
    category = await session.get(Category, category_id)
    return category


async def get_category_by_id_extended_crud(
    category_id: int, query_parametrs: str, session: AsyncSession, user_db: User
):

    params = "transactions"
    query_parametrs = query_parametrs.strip().lower()

    current_category = await session.get(Category, category_id)
    if current_category is None:
        return None
    if current_category.user_id != user_db.id and current_category.user_id is not None:
        raise GetCategoryForbidden
    if query_parametrs == params:
        stmt = (
            select(Transaction)
            .filter(
                Transaction.user_id == user_db.id,
                Transaction.category_id == category_id,
            )
            .order_by(Transaction.id)
        )
        result = await session.execute(stmt)
        transactions = result.scalars().all()
        return build_response_category(
            current_object=current_category, transactions_override=transactions
        )
    return build_response_category(current_object=current_category)


async def get_list_category_crud(
    session: AsyncSession,
    start: int = 0,
    stop: int = 3,
):
    stmt = select(Category).order_by(Category.id).limit(stop - start).offset(start)
    result = await session.execute(stmt)
    categories: list = result.scalars().all()
    return categories


async def update_category_crud(
    category_id: int,
    category_data: UpdateCategory,
    session: AsyncSession,
    user_db: User,
):
    current_category = await get_category_by_id_crud(
        category_id=category_id, session=session
    )
    if current_category is None:
        return None
    if current_category.user_id is None:
        raise GetSharedCategoryForbidden
    if current_category.user_id != user_db.id:
        raise GetCategoryForbidden
    update_category = category_data.model_dump()
    for k, v in update_category.items():
        setattr(current_category, k, v)
    await session.commit()
    await session.refresh(current_category)
    return current_category


async def delete_category_crud(user_db: User, category_id: int, session: AsyncSession):
    delete_category = await get_category_by_id_crud(
        category_id=category_id, session=session
    )
    if delete_category is None:
        return None
    if delete_category.user_id is None:
        raise GetSharedCategoryForbidden
    if delete_category.user_id != user_db.id:
        raise GetCategoryForbidden
    await session.delete(delete_category)
    await session.commit()
    return {"message": "delete"}
