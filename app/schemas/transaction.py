from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime


class CreateTransaction(BaseModel):
    amount: float = Field(ge=1)
    category_id: int
    user_id: int
    description: str
    transaction_date: date


class ResponseTransaction(CreateTransaction):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
