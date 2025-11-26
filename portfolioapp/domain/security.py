from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from portfolioapp.database import Base

class Security(Base):
    __tablename__ = "security"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(10), unique=True)
    issuer: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)

    def __repr__(self):
        return f"<Security {self.ticker} price={self.price}>"

