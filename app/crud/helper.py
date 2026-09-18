from app.models.transaction import Transaction

from app.models.category import Category
from app.models.user import User
from app.schemas.user import (
    ResponseUserCost,
    ResponseCategoryPercentage,
    ResponseUserExtended,
    ResponseUserTopCost,
    ResponseComparisonTransactionByMonth,
)
from app.schemas.category import ResponseCategoryExtended
import calendar
from datetime import date


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


def build_response_percentage_user_transactions(data_in: list[tuple]):
    response = []
    for e in data_in:
        convert_data = ResponseCategoryPercentage(
            сategory_name=e[0],
            percentage=e[1],
        )
        response.append(convert_data)
    return response


def build_response_comparison(data: list[dict]):
    result = []
    for obj in data:
        result.append(ResponseComparisonTransactionByMonth(**obj))
    return result


def calculate_percentage_difference_by_month(
    prev_month_data: list[tuple], curr_month_data: list[tuple]
):
    result = []
    prev_data: dict = convert_data_in_dict(prev_month_data)
    curr_data: dict = convert_data_in_dict(curr_month_data)
    all_data: set = set(prev_data.keys()) | set(curr_data.keys())
    for category_id in all_data:
        sum_prev = prev_data.get(category_id, 0)
        sum_curr = curr_data.get(category_id, 0)
        if sum_curr != 0 and sum_prev != 0:
            percantage = (sum_curr - sum_prev) / sum_prev * 100
            result.append(
                {
                    "category_id": category_id,
                    "sum_prev": sum_prev,
                    "sum_curr": sum_curr,
                    "percentage": percantage,
                }
            )
        elif sum_prev == 0 and sum_curr > 0:
            result.append(
                {
                    "category_id": category_id,
                    "sum_prev": sum_prev,
                    "sum_curr": sum_curr,
                    "status": "Новая затрата",
                }
            )
        elif sum_prev > 0 and sum_curr == 0:
            result.append(
                {
                    "category_id": category_id,
                    "sum_prev": sum_prev,
                    "sum_curr": sum_curr,
                    "status": "Старая затрата",
                }
            )
    return result


def convert_data_in_dict(data: list[tuple]):
    result = {}
    for elem in data:
        result[elem[0]] = elem[1]
    return result


def get_date_helper(
    prev_month: date,
    curr_month: date,
):
    start_current_month = curr_month.replace(day=1)
    start_previous_month = prev_month.replace(day=1)
    # количество дней
    last_day_number_prev_month: int = calendar.monthrange(
        prev_month.year, prev_month.month
    )[1]
    last_day_number_curr_month: int = calendar.monthrange(
        curr_month.year, curr_month.month
    )[1]
    end_prev_month = date(prev_month.year, prev_month.month, last_day_number_prev_month)
    end_curr_month = date(curr_month.year, curr_month.month, last_day_number_curr_month)
    return {
        "start_prev_month": start_previous_month,
        "start_curr_month": start_current_month,
        "end_prev_month": end_prev_month,
        "end_curr_month": end_curr_month,
    }
