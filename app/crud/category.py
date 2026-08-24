from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.category import CreateCategory, UpdateCategory
from app.models.category import Category
from app.crud import user
from sqlalchemy import select


async def create_category_crud(category_data: CreateCategory, session: AsyncSession):
    if category_data.user_id is not None:
        current_user = await user.get_user_by_id_crud(
            user_id=category_data.user_id, session=session
        )
        if current_user is None:
            return None

    new_category = Category(**category_data.model_dump())
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category


async def get_category_by_id_crud(category_id: int, session: AsyncSession):
    current_category = await session.get(Category, category_id)
    return current_category


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
    category_id: int, category_data: UpdateCategory, session: AsyncSession
):
    current_category = await get_category_by_id_crud(
        category_id=category_id, session=session
    )
    if current_category is None:
        return None
    update_category = category_data.model_dump()
    for k, v in update_category.items():
        setattr(current_category, k, v)
    await session.commit()
    await session.refresh(current_category)
    return current_category


async def delete_category_crud(category_id: int, session: AsyncSession):
    current_category = await get_category_by_id_crud(
        category_id=category_id, session=session
    )
    if current_category is None:
        return None
    return {"message": "delete"}
