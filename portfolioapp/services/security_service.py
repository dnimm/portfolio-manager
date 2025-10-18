"""
Security service for business logic operations
"""
from typing import List, Optional
import db
from domain.security import Security
from services.exceptions import ValidationError

class SecurityService:
    """Service class for security-related operations"""
    
    @staticmethod
    def get_all_securities() -> List[Security]:
        """Get all available securities"""
        return list(db.securities.values())
    
    @staticmethod
    def get_security(ticker: str) -> Optional[Security]:
        """Get a security by ticker"""
        if not ticker or not ticker.strip():
            raise ValidationError("Ticker is required")
        return db.securities.get(ticker.upper())
    
    @staticmethod
    def security_exists(ticker: str) -> bool:
        """Check if a security exists"""
        if not ticker or not ticker.strip():
            return False
        return ticker.upper() in db.securities
    
    @staticmethod
    def calculate_order_amount(ticker: str, quantity: int) -> Optional[float]:
        """Calculate total amount for an order"""
        try:
            if quantity <= 0:
                raise ValidationError("Quantity must be positive")
            
            security = SecurityService.get_security(ticker)
            if not security:
                return None
            return security.price * quantity
        except Exception as e:
            raise ValidationError(f"Failed to calculate order amount: {e}")