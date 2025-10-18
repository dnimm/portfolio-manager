"""
Investment domain model
"""
from dataclasses import dataclass

@dataclass
class Investment:
    """Represents an investment holding in a portfolio"""
    ticker: str
    quantity: int
    purchase_price: float
    
    def __post_init__(self):
        """Validate investment data after initialization"""
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.purchase_price <= 0:
            raise ValueError("Purchase price must be positive")
    
    @property
    def total_value(self) -> float:
        """Calculate total value of this investment"""
        return self.quantity * self.purchase_price