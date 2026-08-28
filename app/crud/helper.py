from app.models.category import Category
from app.models.user import User
from app.schemas.user import ResponseUserCost, ResponseUserExtended
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


def build_response_user_cost(
    data_in: list,
):
    result = []
    for d in data_in:
        convert_data = ResponseUserCost(category_id=d[0], total_amount_by_category=d[1])
        result.append(convert_data)
    return result
