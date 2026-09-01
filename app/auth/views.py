from fastapi import APIRouter, Depends

from app.models.user import User
from app.schemas.token import ResponseToken
from app.auth.dependencies import user_auth, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=ResponseToken)
async def login(current_user: User = Depends(user_auth)):

    token = create_access_token(current_user=current_user)
    return ResponseToken(
        access_token=token,
    )
