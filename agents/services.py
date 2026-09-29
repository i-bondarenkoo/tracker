from sqlalchemy import select

from app.models.category import Category


async def get_all_category(category_ids: list[int], session):
    stmt = select(Category).filter(Category.id.in_(category_ids))
    result = await session.execute(stmt)
    categories = result.scalars().all()
    return categories
