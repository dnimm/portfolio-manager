from app.db import db
from sqlalchemy import String, Float

class User(db.Model):
    __tablename__ = "user"

    username = db.Column(String(100), primary_key=True)
    password = db.Column(String(100))
    firstname = db.Column(String(100))
    lastname = db.Column(String(100))
    balance = db.Column(Float)

    portfolios = db.relationship("Portfolio", back_populates="user")
    transactions = db.relationship("Transaction", back_populates="user")

    def __to_dict__(self):
        return {
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "balance": self.balance,
        }