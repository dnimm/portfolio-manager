from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from portfolioapp.database import Base

if TYPE_CHECKING:
    from domain.user import User
    from domain.investment import Investment
    from domain.transaction import Transaction

class Portfolio(Base):
    __tablename__ = "portfolio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(200))

    
    owner_username: Mapped[str] = mapped_column(
        ForeignKey("user.username")
    )

    user: Mapped["User"] = relationship(
        back_populates="portfolios"
    )

    investments: Mapped[List["Investment"]] = relationship(
        back_populates="portfolio"
    )

    transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="portfolio"
    )

    def __repr__(self):
        return f"<Portfolio id={self.id} name={self.name}>"

