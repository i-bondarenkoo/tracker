from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings


class DataBaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def close_session(self):
        if self.engine is not None:
            return await self.engine.dispose()

    async def get_session(self):
        async with self.session_factory() as session:
            yield session


db_helper = DataBaseHelper(url=settings.db_url, echo=settings.db_echo)
