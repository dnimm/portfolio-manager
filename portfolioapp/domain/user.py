"""
User domain model
"""
from dataclasses import dataclass

@dataclass
class User:
    """Represents a user in the system"""
    first_name: str
    last_name: str
    username: str
    password: str
    balance: float
    
    def __post_init__(self):
        """Validate user data after initialization"""
        if self.balance < 0:
            raise ValueError("Balance cannot be negative")
    
    def update_balance(self, amount: float) -> bool:
        """Update user balance with validation"""
        new_balance = self.balance + amount
        if new_balance < 0:
            return False
        self.balance = new_balance
        return True
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"