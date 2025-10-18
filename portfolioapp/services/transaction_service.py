"""
Transaction service for handling transaction history
"""
from typing import List
import db
from domain.transaction import Transaction

class TransactionService:
    """Service class for transaction-related operations"""
    
    @staticmethod
    def get_user_transactions(username: str) -> List[Transaction]:
        """Get all transactions for a user"""
        return db.get_user_transactions(username)
    
    @staticmethod
    def get_recent_transactions(username: str, limit: int = 10) -> List[Transaction]:
        """Get recent transactions for a user"""
        transactions = db.get_user_transactions(username)
        return sorted(transactions, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    @staticmethod
    def get_transactions_by_portfolio(username: str, portfolio_id: int) -> List[Transaction]:
        """Get transactions for a specific portfolio"""
        transactions = db.get_user_transactions(username)
        return [t for t in transactions if t.portfolio_id == portfolio_id]