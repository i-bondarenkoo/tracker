from pydantic import EmailStr

from app.db.db_helper import db_helper
from app.schemas.user import UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user
from app.models.user import User
from app.auth.service import check_password
from app.auth.jwt import encode_jwt
from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt import decode_jwt
from jwt.exceptions import InvalidTokenError
from app.auth.service import check_password
from app.auth.security import oauth2_scheme


async def get_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        token_data: dict = decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        print(f"ERROR: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователь не авторизован",
        )
    return token_data


async def get_current_user(
    token_data: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_helper.get_session),
):
    user_id: int = token_data["id"]
    # email: EmailStr = token_data['email']
    current_user = await user.get_user_by_id_crud(user_id=user_id, session=session)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован",
        )
    return current_user


async def user_auth(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.get_session),
):
    current_user = await user.get_user_by_email_crud(email=username, session=session)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован",
        )
    check_pass = check_password(
        password=password, hashed_password=current_user.password_hash
    )
    if not check_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован",
        )
    return current_user


def create_access_token(current_user: User):
    payload = {"email": current_user.email, "id": current_user.id}
    access_token = encode_jwt(payload=payload)
    return access_token
