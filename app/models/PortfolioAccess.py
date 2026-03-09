from app.db import db
from sqlalchemy import Integer, String, ForeignKey


class PortfolioAccess(db.Model):
    __tablename__ = "portfolio_access"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(Integer, ForeignKey("portfolio.id"), nullable=False)
    username = db.Column(String(100), ForeignKey("user.username"), nullable=False)
    role = db.Column(String(100), nullable=False)

    def __to_dict__(self):
        return {
            "portfolio_id": self.portfolio_id,
            "username": self.username,
            "role": self.role,
        }