from pydantic import BaseModel, ConfigDict, Field


class CreateCategory(BaseModel):
    name: str
    user_id: int | None = Field(default=None, ge=1)


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
