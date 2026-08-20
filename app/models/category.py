from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.transaction import Transaction


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    user: Mapped["User | None"] = relationship(
        "User",
        back_populates="categories",
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="category",
        cascade="all, delete-orphan",
    )
