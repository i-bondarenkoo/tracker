from datetime import datetime, timedelta, timezone

import jwt
from app.core.config import settings


def encode_jwt(
    payload: dict,
    key: str = settings.jwt_auth.key,
    algorithm: str = settings.jwt_auth.algorithm,
    expire_minutes: int = settings.jwt_auth.access_token_expire_minutes,
) -> bytes:
    to_encode: dict = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        # время создания токена
        iat=now,
        # время до которого токен действителен
        exp=expire,
    )
    token = jwt.encode(payload=to_encode, key=key, algorithm=algorithm)
    return token


def decode_jwt(
    token: str,
    key: str = settings.jwt_auth.key,
    algorithm: str = settings.jwt_auth.algorithm,
) -> str:
    decoded_token = jwt.decode(
        jwt=token,
        key=key,
        algorithms=[algorithm],
    )
    return decoded_token
