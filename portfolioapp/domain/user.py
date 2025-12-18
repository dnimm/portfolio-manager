from portfolioapp.db import db

class User(db.Model):
    __tablename__ = "user"

    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, default=0.0)

    portfolios = db.relationship("Portfolio", backref="user", cascade="all, delete-orphan")
