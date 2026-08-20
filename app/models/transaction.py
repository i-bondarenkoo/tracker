from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String, func, Date
from typing import TYPE_CHECKING
from datetime import datetime, date

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.category import Category


class Transaction(Base):
    __tablename__ = "transactions"

    amount: Mapped[float]
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )
    description: Mapped[str] = mapped_column(String(100))
    transaction_date: Mapped[date] = mapped_column(Date, default=date.today)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    user: Mapped["User"] = relationship("User", back_populates="transactions")
    category: Mapped["Category"] = relationship(
        "Category", back_populates="transactions"
    )
