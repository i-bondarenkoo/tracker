from app.models.category import Category
from app.models.user import User
from app.schemas.user import ResponseUserExtended
from app.schemas.category import ResponseCategoryExtended


def build_response(current_object: User | Category, requested: set[str]):
    if isinstance(current_object, User):
        return ResponseUserExtended(
            id=current_object.id,
            first_name=current_object.first_name,
            last_name=current_object.last_name,
            email=current_object.email,
            categories=current_object.categories if "categories" in requested else None,
            transactions=(
                current_object.transactions if "transactions" in requested else None
            ),
        )
    else:
        return ResponseCategoryExtended(
            id=current_object.id,
            name=current_object.name,
            user_id=current_object.user_id,
            transactions=(
                current_object.transactions if "transactions" in requested else None
            ),
        )
