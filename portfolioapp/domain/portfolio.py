"""
Portfolio domain model
"""
from dataclasses import dataclass, field
from typing import List, Dict
from domain.investment import Investment
from domain.security import Security

@dataclass
class Portfolio:
    """Represents an investment portfolio"""
    id: int
    name: str
    description: str
    holdings: List[Investment] = field(default_factory=list)
    
    def add_investment(self, investment: Investment) -> None:
        """Add an investment to the portfolio"""
        self.holdings.append(investment)
    
    def remove_investment(self, ticker: str) -> bool:
        """Remove an investment completely from the portfolio"""
        for i, investment in enumerate(self.holdings):
            if investment.ticker == ticker:
                del self.holdings[i]
                return True
        return False
    
    def get_investment(self, ticker: str) -> Investment | None:
        """Get an investment by ticker symbol"""
        for investment in self.holdings:
            if investment.ticker == ticker:
                return investment
        return None
    
    def update_investment_quantity(self, ticker: str, new_quantity: int) -> bool:
        """Update the quantity of an existing investment"""
        investment = self.get_investment(ticker)
        if investment:
            investment.quantity = new_quantity
            return True
        return False
    
    def has_holdings(self) -> bool:
        """Check if portfolio has any investments"""
        return len(self.holdings) > 0
    
    def get_total_value(self, current_prices: Dict[str, float]) -> float:
        """Calculate total current value of all holdings"""
        total = 0.0
        for investment in self.holdings:
            current_price = current_prices.get(investment.ticker, investment.purchase_price)
            total += investment.quantity * current_price
        return total
    
    def get_total_cost(self) -> float:
        """Calculate total cost basis of all holdings"""
        return sum(investment.quantity * investment.purchase_price 
                  for investment in self.holdings)
    
    def get_unrealized_gain_loss(self, current_prices: Dict[str, float]) -> float:
        """Calculate unrealized gain/loss"""
        total_value = self.get_total_value(current_prices)
        total_cost = self.get_total_cost()
        return total_value - total_cost
    
    def get_performance_percentage(self, current_prices: Dict[str, float]) -> float:
        """Calculate performance as percentage"""
        total_cost = self.get_total_cost()
        if total_cost == 0:
            return 0.0
        gain_loss = self.get_unrealized_gain_loss(current_prices)
        return (gain_loss / total_cost) * 100
    
    def get_sector_breakdown(self, securities: Dict[str, Security]) -> Dict[str, float]:
        """Get portfolio breakdown by sector"""
        sector_value: Dict[str, float] = {}
        total_value = self.get_total_cost()
        
        for investment in self.holdings:
            security = securities.get(investment.ticker)
            if security:
                sector = self._get_sector_from_issuer(security.issuer)
                investment_value = investment.quantity * investment.purchase_price
                sector_value[sector] = sector_value.get(sector, 0.0) + investment_value
        
        # Convert to percentages
        if total_value > 0:
            for sector in sector_value:
                sector_value[sector] = (sector_value[sector] / total_value) * 100
        
        return sector_value
    
    def _get_sector_from_issuer(self, issuer: str) -> str:
        """Determine sector based on issuer name"""
        issuer_lower = issuer.lower()
        if any(tech in issuer_lower for tech in ['apple', 'google', 'microsoft', 'amazon', 'tesla', 'nvidia', 'meta', 'netflix']):
            return "Technology"
        elif any(finance in issuer_lower for finance in ['bank', 'chase', 'visa', 'mastercard']):
            return "Financial"
        elif any(health in issuer_lower for health in ['johnson', 'pfizer', 'health']):
            return "Healthcare"
        elif any(consumer in issuer_lower for consumer in ['coca', 'procter', 'gamble', 'walmart']):
            return "Consumer"
        else:
            return "Other"