from app.db import db
from sqlalchemy import Integer, String, ForeignKey

class Portfolio(db.Model):
    __tablename__ = "portfolio"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(100), nullable=False)
    description = db.Column(String(500))
    owner = db.Column(String(100), db.ForeignKey("user.username"))

    user = db.relationship("User", back_populates="portfolios")
    investments = db.relationship("Investment", back_populates="portfolio", cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", back_populates="portfolio")

    def __to_dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
        }