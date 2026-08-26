from app.models.user import User
from app.schemas.user import ResponseUserExtended


def build_response(current_user: User, requested: set[str]):
    return ResponseUserExtended(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        categories=current_user.categories if "categories" in requested else None,
        transactions=current_user.transactions if "transactions" in requested else None,
    )
