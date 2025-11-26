from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, ForeignKey
from portfolioapp.database import Base

class Investment(Base):
    __tablename__ = "investment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.id"))
    ticker: Mapped[str] = mapped_column(String(20))
    quantity: Mapped[int] = mapped_column(Integer)
    purchase_price: Mapped[float] = mapped_column(Float)

    portfolio = relationship("Portfolio", back_populates="investments")

    def __repr__(self):
        return f"<Investment ticker={self.ticker} qty={self.quantity}>"

