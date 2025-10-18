"""
Mock database module for storing application data
"""
from typing import Dict, List, Optional
from domain.user import User
from domain.portfolio import Portfolio
from domain.security import Security
from domain.transaction import Transaction
from services.exceptions import DatabaseError, ValidationError

# Database storage
users: Dict[str, User] = {}
portfolios: Dict[str, List[Portfolio]] = {}  # username -> list of portfolios
securities: Dict[str, Security] = {}
transactions: Dict[str, List[Transaction]] = {}  # username -> list of transactions
logged_in_user: Optional[User] = None
next_portfolio_id: int = 1
next_transaction_id: int = 1

def initialize_data():
    """Initialize the database with default data"""
    global users, securities, next_portfolio_id, next_transaction_id
    
    # Create admin user
    admin = User("Admin", "User", "admin", "admin123", 10000.0)
    users["admin"] = admin
    
    # Create predefined users
    predefined_users = [
        User("Sarah", "Johnson", "sarahj", "pass123", 15000.0),
        User("Mike", "Chen", "mikec", "pass123", 8000.0),
        User("Emma", "Wilson", "emmaw", "pass123", 12000.0)
    ]
    
    for user in predefined_users:
        users[user.username] = user
        portfolios[user.username] = []
        transactions[user.username] = []
    
    # Create extensive securities list
    tech_stocks = [
        Security("AAPL", "Apple Inc.", 150.0),
        Security("GOOGL", "Alphabet Inc.", 2800.0),
        Security("MSFT", "Microsoft Corporation", 300.0),
        Security("AMZN", "Amazon.com Inc.", 3300.0),
        Security("TSLA", "Tesla Inc.", 700.0),
        Security("NVDA", "NVIDIA Corporation", 450.0),
        Security("META", "Meta Platforms Inc.", 320.0),
        Security("NFLX", "Netflix Inc.", 380.0)
    ]
    
    finance_stocks = [
        Security("JPM", "JPMorgan Chase & Co.", 160.0),
        Security("BAC", "Bank of America Corp.", 35.0),
        Security("V", "Visa Inc.", 220.0),
        Security("MA", "Mastercard Inc.", 350.0)
    ]
    
    healthcare_stocks = [
        Security("JNJ", "Johnson & Johnson", 165.0),
        Security("PFE", "Pfizer Inc.", 45.0),
        Security("UNH", "UnitedHealth Group Inc.", 520.0)
    ]
    
    consumer_stocks = [
        Security("KO", "The Coca-Cola Company", 60.0),
        Security("PG", "Procter & Gamble Co.", 145.0),
        Security("WMT", "Walmart Inc.", 155.0)
    ]
    
    # Add all securities to database
    all_securities = tech_stocks + finance_stocks + healthcare_stocks + consumer_stocks
    for security in all_securities:
        securities[security.ticker] = security
    
    # Reset counters
    next_portfolio_id = 1
    next_transaction_id = 1

def get_next_portfolio_id() -> int:
    """Get the next available portfolio ID"""
    global next_portfolio_id
    current_id = next_portfolio_id
    next_portfolio_id += 1
    return current_id

def get_next_transaction_id() -> int:
    """Get the next available transaction ID"""
    global next_transaction_id
    current_id = next_transaction_id
    next_transaction_id += 1
    return current_id

def add_user(user: User) -> bool:
    """Add a new user to the database"""
    if user.username in users:
        return False
    users[user.username] = user
    portfolios[user.username] = []
    transactions[user.username] = []
    return True

def delete_user(username: str) -> bool:
    """Delete a user from the database"""
    if username not in users:
        return False
    
    # Check if user has existing portfolios with holdings
    if username in portfolios:
        user_portfolios = portfolios[username]
        for portfolio in user_portfolios:
            if portfolio.has_holdings():
                return False  # User has portfolios with investments
    
    del users[username]
    if username in portfolios:
        del portfolios[username]
    if username in transactions:
        del transactions[username]
    return True

def get_user_portfolios(username: str) -> List[Portfolio]:
    """Get all portfolios for a user"""
    return portfolios.get(username, [])

def add_portfolio(username: str, portfolio: Portfolio) -> bool:
    """Add a portfolio for a user"""
    if username not in portfolios:
        portfolios[username] = []
    portfolios[username].append(portfolio)
    return True

def delete_portfolio(username: str, portfolio_id: int) -> bool:
    """Delete a portfolio for a user"""
    if username not in portfolios:
        return False
    
    user_portfolios = portfolios[username]
    for i, portfolio in enumerate(user_portfolios):
        if portfolio.id == portfolio_id:
            if portfolio.has_holdings():  # Check if portfolio has investments
                return False
            del user_portfolios[i]
            return True
    return False

def get_portfolio_by_id(username: str, portfolio_id: int) -> Optional[Portfolio]:
    """Get a specific portfolio by ID for a user"""
    if username not in portfolios:
        return None
    
    for portfolio in portfolios[username]:
        if portfolio.id == portfolio_id:
            return portfolio
    return None

def add_transaction(username: str, transaction: Transaction) -> None:
    """Add a transaction to user's history"""
    if username not in transactions:
        transactions[username] = []
    transactions[username].append(transaction)

def get_user_transactions(username: str) -> List[Transaction]:
    """Get all transactions for a user"""
    return transactions.get(username, [])

# Initialize data when module is imported
initialize_data()