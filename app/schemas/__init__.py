from app.schemas.user import (
    CreateUser,
    ResponseUser,
    # ResponseUserWithCategories,
    UpdateUserPatch,
    UpdateUserFull,
    # ResponseUserWithTransactions,
    ResponseUserExtended,
    ResponseUserCost,
    UserLogin,
    ResponseUserAvgValue,
)
from app.schemas.category import (
    CreateCategory,
    ResponseCategory,
    UpdateCategory,
    ResponseCategoryShort,
    ResponseCategoryExtended,
)
from app.schemas.transaction import (
    CreateTransaction,
    ResponseTransaction,
    UpdateTransaction,
    ResponseTransactionShort,
    ResponseTransactionShortWithUserID,
)
from app.schemas.token import ResponseToken

# ResponseUserWithCategories.model_rebuild()
# ResponseUserWithTransactions.model_rebuild()
ResponseUserExtended.model_rebuild()
ResponseCategoryExtended.model_rebuild()
