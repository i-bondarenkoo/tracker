from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.category import ResponseCategoryShort
    from app.schemas.transaction import ResponseTransactionShort


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class CreateUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class ResponseUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateUserPatch(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UpdateUserFull(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


# class ResponseUserWithCategories(BaseModel):
#     id: int
#     first_name: str
#     last_name: str
#     email: EmailStr
#     # created_at: datetime
#     categories: list["ResponseCategoryShort"]
#     model_config = ConfigDict(from_attributes=True)


# class ResponseUserWithTransactions(BaseModel):
#     id: int
#     first_name: str
#     last_name: str
#     email: EmailStr
#     transactions: list["ResponseTransactionShort"]
#     model_config = ConfigDict(from_attributes=True)


class ResponseUserExtended(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    categories: list["ResponseCategoryShort"] | None = None
    transactions: list["ResponseTransactionShort"] | None = None

    model_config = ConfigDict(from_attributes=True)


class ResponseUserCost(BaseModel):
    category_id: int
    total_amount_by_category: float

    model_config = ConfigDict(from_attributes=True)


class ResponseUserTopCost(BaseModel):
    name: str
    category_id: int
    total_amount_by_category: float = Field(ge=1)

    model_config = ConfigDict(from_attributes=True)


class ResponseUserAvgValue(BaseModel):
    id: int
    amount: int
    cost: float
    category_id: int
    user_id: int
    description: str
    transaction_date: date
    model_config = ConfigDict(from_attributes=True)
