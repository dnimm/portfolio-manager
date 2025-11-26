from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float
from portfolioapp.database import Base

if TYPE_CHECKING:
    from domain.portfolio import Portfolio

class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(50), primary_key=True)
    password: Mapped[str] = mapped_column(String(50))
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    balance: Mapped[float] = mapped_column(Float)

    portfolios: Mapped[List["Portfolio"]] = relationship(
        back_populates="user"
    )

    def __repr__(self):
        return f"<User username={self.username} name={self.firstname} {self.lastname}>"

