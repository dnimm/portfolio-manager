from portfolioapp.db import db

class Investment(db.Model):
    __tablename__ = "investment"

    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey("portfolio.id"))
    ticker = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    purchase_price = db.Column(db.Float)
