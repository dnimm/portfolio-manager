from app.db import db
from sqlalchemy import Integer, String, ForeignKey

class Investment(db.Model):
    __tablename__ = "investment"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(Integer, db.ForeignKey("portfolio.id"))
    ticker = db.Column(String(100), db.ForeignKey("security.ticker"))
    quantity = db.Column(Integer)

    portfolio = db.relationship("Portfolio", back_populates="investments")
    security = db.relationship("Security", back_populates="investments")

    def __to_dict__(self):
        return {
            "id": self.id,
            "portfolio_id": self.portfolio_id,
            "ticker": self.ticker,
            "quantity": self.quantity,
        }