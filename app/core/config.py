from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class JWTAuth(BaseModel):
    algorithm: str
    key: str
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    db_url: str
    db_echo: bool
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )
    jwt_auth: JWTAuth


settings = Settings()
