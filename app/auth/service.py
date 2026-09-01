import bcrypt


def hash_password(password: str) -> bytes:
    salt: bytes = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
