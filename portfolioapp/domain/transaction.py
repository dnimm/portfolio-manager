from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, DateTime, ForeignKey
from portfolioapp.database import Base

class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.id"))
    ticker: Mapped[str] = mapped_column(String(20))
    txn_type: Mapped[str] = mapped_column(String(10))    
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )

    portfolio = relationship("Portfolio", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.txn_type} {self.ticker} {self.quantity}>"


