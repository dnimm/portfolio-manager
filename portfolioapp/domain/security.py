"""
Security domain model
"""
from dataclasses import dataclass

@dataclass
class Security:
    """Represents a security available for investment"""
    ticker: str
    issuer: str
    price: float
    
    def __post_init__(self):
        """Validate security data after initialization"""
        if self.price <= 0:
            raise ValueError("Price must be positive")