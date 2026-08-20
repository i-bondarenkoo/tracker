from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.transaction import Transaction


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(35))
    last_name: Mapped[str] = mapped_column(String(35))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        # на стороне бд
        server_default=func.now(),
        # на стороне алхимии
        default=datetime.now,
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan",
    )
