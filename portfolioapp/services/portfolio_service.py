"""
Portfolio service for business logic operations
"""
from typing import List, Optional, Tuple, Dict
from datetime import datetime
import db
from domain.portfolio import Portfolio
from domain.investment import Investment
from domain.security import Security
from domain.transaction import Transaction
from services.exceptions import PortfolioError, InvestmentError, ValidationError

class PortfolioService:
    """Service class for portfolio-related operations"""
    
    @staticmethod
    def get_user_portfolios(username: str) -> List[Portfolio]:
        """Get all portfolios for a user"""
        try:
            return db.get_user_portfolios(username)
        except Exception as e:
            raise PortfolioError(f"Failed to get user portfolios: {e}")
    
    @staticmethod
    def create_portfolio(username: str, name: str, description: str) -> Tuple[bool, str]:
        """Create a new portfolio for a user"""
        try:
            if not name or not name.strip():
                return False, "Portfolio name cannot be empty"
            if not description or not description.strip():
                return False, "Portfolio description cannot be empty"
            
            portfolio_id = db.get_next_portfolio_id()
            portfolio = Portfolio(portfolio_id, name.strip(), description.strip())
            
            if db.add_portfolio(username, portfolio):
                return True, f"Portfolio '{name}' created successfully with ID: {portfolio_id}"
            else:
                return False, "Failed to create portfolio"
        except Exception as e:
            return False, f"Error creating portfolio: {e}"
    
    @staticmethod
    def delete_portfolio(username: str, portfolio_id: int) -> Tuple[bool, str]:
        """Delete a portfolio"""
        try:
            if portfolio_id <= 0:
                return False, "Invalid portfolio ID"
            
            portfolio = db.get_portfolio_by_id(username, portfolio_id)
            if not portfolio:
                return False, "Portfolio not found"
            
            if portfolio.has_holdings():
                return False, "Cannot delete portfolio with existing investments"
            
            if db.delete_portfolio(username, portfolio_id):
                return True, "Portfolio deleted successfully"
            else:
                return False, "Failed to delete portfolio"
        except Exception as e:
            return False, f"Error deleting portfolio: {e}"
    
    @staticmethod
    def add_investment(portfolio: Portfolio, security: Security, quantity: int) -> Tuple[bool, str]:
        """Add an investment to a portfolio"""
        try:
            if quantity <= 0:
                return False, "Quantity must be positive"
            
            # Check if investment already exists
            existing_investment = portfolio.get_investment(security.ticker)
            
            if existing_investment:
                # Update existing investment (average price)
                total_quantity = existing_investment.quantity + quantity
                total_cost = (existing_investment.total_value + 
                             quantity * security.price)
                average_price = total_cost / total_quantity
                
                existing_investment.quantity = total_quantity
                existing_investment.purchase_price = average_price
            else:
                # Create new investment
                investment = Investment(security.ticker, quantity, security.price)
                portfolio.add_investment(investment)
            
            return True, "Investment added successfully"
        except Exception as e:
            return False, f"Error adding investment: {e}"
    
    @staticmethod
    def liquidate_investment(portfolio: Portfolio, ticker: str, quantity: int, 
                           sale_price: float) -> Tuple[bool, str, float]:
        """Liquidate an investment from a portfolio"""
        try:
            if not ticker or not ticker.strip():
                return False, "Ticker is required", 0.0
            if quantity <= 0:
                return False, "Quantity must be positive", 0.0
            if sale_price <= 0:
                return False, "Sale price must be positive", 0.0
            
            ticker = ticker.strip().upper()
            investment = portfolio.get_investment(ticker)
            if not investment:
                return False, "Investment not found in portfolio", 0.0
            
            if quantity > investment.quantity:
                return False, f"Insufficient shares. You have {investment.quantity} shares", 0.0
            
            # Calculate sale proceeds
            sale_proceeds = quantity * sale_price
            
            if quantity == investment.quantity:
                # Full liquidation - remove investment
                portfolio.remove_investment(ticker)
                message = "Full liquidation completed"
            else:
                # Partial liquidation - update quantity
                investment.quantity -= quantity
                message = f"Partial liquidation completed. {investment.quantity} shares remaining"
            
            return True, message, sale_proceeds
        except Exception as e:
            return False, f"Error liquidating investment: {e}", 0.0
    
    @staticmethod
    def get_portfolio_performance(portfolio: Portfolio) -> Dict[str, float]:
        """Get portfolio performance metrics"""
        try:
            current_prices = {ticker: security.price for ticker, security in db.securities.items()}
            
            total_cost = portfolio.get_total_cost()
            current_value = portfolio.get_total_value(current_prices)
            unrealized_gain_loss = portfolio.get_unrealized_gain_loss(current_prices)
            performance_percentage = portfolio.get_performance_percentage(current_prices)
            
            return {
                "total_cost": total_cost,
                "current_value": current_value,
                "unrealized_gain_loss": unrealized_gain_loss,
                "performance_percentage": performance_percentage
            }
        except Exception as e:
            raise PortfolioError(f"Failed to calculate portfolio performance: {e}")
    
    @staticmethod
    def get_portfolio_analytics(portfolio: Portfolio) -> Dict[str, float]:
        """Get portfolio analytics including sector breakdown"""
        try:
            sector_breakdown = portfolio.get_sector_breakdown(db.securities)
            return sector_breakdown
        except Exception as e:
            raise PortfolioError(f"Failed to get portfolio analytics: {e}")
    
    @staticmethod
    def record_transaction(username: str, transaction_type: str, ticker: str, 
                         quantity: int, price: float, total_amount: float, 
                         portfolio_id: int) -> None:
        """Record a transaction in user's history"""
        try:
            transaction_id = db.get_next_transaction_id()
            transaction = Transaction(
                id=transaction_id,
                type=transaction_type,
                ticker=ticker,
                quantity=quantity,
                price=price,
                total_amount=total_amount,
                portfolio_id=portfolio_id,
                timestamp=datetime.now()
            )
            db.add_transaction(username, transaction)
        except Exception as e:
            raise PortfolioError(f"Failed to record transaction: {e}")