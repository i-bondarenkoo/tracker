from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime


class CreateTransaction(BaseModel):
    amount: float = Field(ge=1)
    category_id: int = Field(ge=1)
    user_id: int = Field(ge=1)
    description: str
    transaction_date: date


class ResponseTransaction(CreateTransaction):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateTransaction(BaseModel):
    amount: float | None = Field(ge=1, default=None)
    description: str | None = None
    transaction_date: date | None = None


class ResponseTransactionShort(BaseModel):
    amount: float = Field(ge=1)
    category_id: int = Field(ge=1)
    description: str
    transaction_date: date
    model_config = ConfigDict(from_attributes=True)
