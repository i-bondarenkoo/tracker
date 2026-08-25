from app.schemas.user import (
    CreateUser,
    ResponseUser,
    ResponseUserWithCategories,
    UpdateUserPatch,
    UpdateUserFull,
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
)

ResponseUserWithCategories.model_rebuild()
