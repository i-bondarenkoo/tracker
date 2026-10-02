from dataclasses import dataclass
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class AgentContext:
    user_db: User
    session: AsyncSession
