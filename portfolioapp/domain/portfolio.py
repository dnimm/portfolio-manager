from portfolioapp.db import db

class Portfolio(db.Model):
    __tablename__ = "portfolio"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    owner_username = db.Column(db.String(50), db.ForeignKey("user.username"))

    investments = db.relationship("Investment", cascade="all, delete-orphan")
    transactions = db.relationship("Transaction", cascade="all, delete-orphan")
