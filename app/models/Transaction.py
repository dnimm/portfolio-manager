from app.db import db
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
import datetime

class Transaction(db.Model):
    __tablename__ = "transaction"

    transaction_id = db.Column(Integer, primary_key=True, autoincrement=True)
    username = db.Column(String(100), db.ForeignKey("user.username"))
    portfolio_id = db.Column(Integer, db.ForeignKey("portfolio.id"))
    ticker = db.Column(String(100), db.ForeignKey("security.ticker"))
    transaction_type = db.Column(String(20))
    quantity = db.Column(Integer)
    price = db.Column(Float)
    date_time = db.Column(DateTime, default=datetime.datetime.utcnow)

    portfolio = db.relationship("Portfolio", back_populates="transactions")
    user = db.relationship("User", back_populates="transactions")
    security = db.relationship("Security", back_populates="transactions")

    def __to_dict__(self):
        return {
            "transaction_id": self.transaction_id,
            "username": self.username,
            "portfolio_id": self.portfolio_id,
            "ticker": self.ticker,
            "transaction_type": self.transaction_type,
            "quantity": self.quantity,
            "price": self.price,
            "date_time": self.date_time.isoformat() if self.date_time else None,
        }