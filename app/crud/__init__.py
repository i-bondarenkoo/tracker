from app.crud.user import (
    create_user_crud,
    get_user_by_email_crud,
    get_user_by_id_crud,
    update_user_crud,
    get_list_users_crud,
    get_user_by_id_extended_crud,
    # get_user_with_categories_crud,
    get_spending_by_category_crud,
    get_top_spending_by_category_crud,
    get_transactions_average_value_crud,
)

from app.crud.category import (
    create_category_crud,
    get_category_by_id_crud,
    get_list_category_crud,
    update_category_crud,
    delete_category_crud,
    get_category_by_id_extended_crud,
)
from app.crud.transaction import (
    create_transaction_crud,
    get_transaction_by_id_crud,
    get_list_transactions_crud,
    update_transaction_crud,
    delete_transaction_crud,
)
