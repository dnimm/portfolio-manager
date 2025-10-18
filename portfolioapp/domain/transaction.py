"""
Transaction domain model for tracking investment activities
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

@dataclass
class Transaction:
    """Represents an investment transaction"""
    id: int
    type: Literal["BUY", "SELL"]
    ticker: str
    quantity: int
    price: float
    total_amount: float
    portfolio_id: int
    timestamp: datetime
    
    def __post_init__(self):
        """Validate transaction data"""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.price <= 0:
            raise ValueError("Price must be positive")
        if self.total_amount <= 0:
            raise ValueError("Total amount must be positive")