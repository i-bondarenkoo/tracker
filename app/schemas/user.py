from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from app.schemas.category import ResponseCategoryShort


class CreateUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class ResponseUser(CreateUser):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateUserPatch(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UpdateUserFull(CreateUser):
    pass


class ResponseUserWithCategories(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    # created_at: datetime
    categories: list["ResponseCategoryShort"]
