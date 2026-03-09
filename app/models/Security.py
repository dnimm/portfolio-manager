from app.db import db
from sqlalchemy import String, Float

class Security(db.Model):
    __tablename__ = "security"

    ticker = db.Column(String(100), primary_key=True)
    issuer = db.Column(String(100), nullable=False)
    price = db.Column(Float, nullable=False)

    investments = db.relationship("Investment", back_populates="security")
    transactions = db.relationship("Transaction", back_populates="security")

    def __to_dict__(self):
        return {
            "ticker": self.ticker,
            "issuer": self.issuer,
            "price": self.price,
        }