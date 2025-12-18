from portfolioapp.db import db

class Security(db.Model):
    __tablename__ = "security"

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True)
    issuer = db.Column(db.String(100))
    price = db.Column(db.Float)
