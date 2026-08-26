from app.schemas.user import (
    CreateUser,
    ResponseUser,
    # ResponseUserWithCategories,
    UpdateUserPatch,
    UpdateUserFull,
    # ResponseUserWithTransactions,
    ResponseUserExtended,
)
from app.schemas.category import (
    CreateCategory,
    ResponseCategory,
    UpdateCategory,
    ResponseCategoryShort,
)
from app.schemas.transaction import (
    CreateTransaction,
    ResponseTransaction,
    UpdateTransaction,
    ResponseTransactionShort,
)

# ResponseUserWithCategories.model_rebuild()
# ResponseUserWithTransactions.model_rebuild()
ResponseUserExtended.model_rebuild()
