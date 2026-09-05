from app.models.transaction import Transaction

from app.models.category import Category
from app.models.user import User
from app.schemas.user import ResponseUserCost, ResponseUserExtended, ResponseUserTopCost
from app.schemas.category import ResponseCategoryExtended


def build_response_user(current_object: User, requested: set[str]):

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


def build_response_category(
    current_object: Category,
    transactions_override: list[Transaction] | None = None,
):
    return ResponseCategoryExtended(
        id=current_object.id,
        name=current_object.name,
        user_id=current_object.user_id,
        transactions=(
            transactions_override if transactions_override is not None else None
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


def build_response_top_user_cost(data_in: list):
    result = []
    for d in data_in:
        conver_data = ResponseUserTopCost(
            name=d[0],
            category_id=d[1],
            total_amount_by_category=d[2],
        )
        result.append(conver_data)
    return result
