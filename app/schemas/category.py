from pydantic import BaseModel, ConfigDict, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.transaction import ResponseTransactionShortWithUserID


class CreateCategory(BaseModel):
    name: str
    is_shared: bool = False


class ResponseCategory(BaseModel):
    id: int
    name: str
    user_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateCategory(BaseModel):
    name: str


class ResponseCategoryShort(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class ResponseCategoryExtended(BaseModel):
    id: int
    name: str
    user_id: int | None = Field(ge=1, default=None)
    transactions: list["ResponseTransactionShortWithUserID"] | None
    model_config = ConfigDict(from_attributes=True)
