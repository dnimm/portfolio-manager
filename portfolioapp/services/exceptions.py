"""
Custom exception classes for the Portfolio Manager application
"""

class PortfolioManagerError(Exception):
    """Base exception class for Portfolio Manager"""
    pass

class AuthenticationError(PortfolioManagerError):
    """Raised when authentication fails"""
    pass

class AuthorizationError(PortfolioManagerError):
    """Raised when user lacks required permissions"""
    pass

class ValidationError(PortfolioManagerError):
    """Raised when input validation fails"""
    pass

class DatabaseError(PortfolioManagerError):
    """Raised when database operations fail"""
    pass

class InsufficientBalanceError(PortfolioManagerError):
    """Raised when user has insufficient balance"""
    pass

class PortfolioError(PortfolioManagerError):
    """Raised when portfolio operations fail"""
    pass

class InvestmentError(PortfolioManagerError):
    """Raised when investment operations fail"""
    pass