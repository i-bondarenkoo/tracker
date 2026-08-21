from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class CreateUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class ResponseUser(CreateUser):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
