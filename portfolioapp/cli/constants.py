
LOGIN_MENU = ["Login", "Exit"]
MAIN_MENU = ["Manage Users", "Manage Portfolios", "Marketplace", "Portfolio Analytics", "Logout"]
USER_MENU = ["View all users", "Create user", "Delete user", "Back to main menu"]
PORTFOLIO_MENU = ["View portfolios", "Create new portfolio", "Sell investment", "Back to main menu"]
MARKETPLACE_MENU = ["View securities", "Buy security", "Back to main menu"]
PORTFOLIO_ANALYTICS_MENU = ["View performance", "Dividend analysis", "Process dividend", "Back to main menu"]


LOGIN_SUCCESS = "✅ Login successful! Welcome {}!"
LOGIN_FAILED = "❌ Invalid username or password."
ACCESS_DENIED = "❌ Access denied. Admin privileges required."
USER_CREATED = "✅ User '{}' created successfully!"
USER_DELETED = "✅ User '{}' deleted successfully!"
PORTFOLIO_CREATED = "✅ Portfolio '{}' created successfully with ID: {}"
PURCHASE_SUCCESS = "✅ Successfully purchased {} shares of {} for ${:.2f}"
SALE_SUCCESS = "✅ Successfully sold {} shares of {} for ${:.2f}"
DIVIDEND_PROCESSED = "✅ Dividend processed successfully! ${:.2f} added to balance."


USERNAME_EXISTS = "❌ Username already exists."
USER_NOT_FOUND = "❌ User not found."
CANNOT_DELETE_SELF = "❌ You cannot delete your own account."
LAST_ADMIN = "❌ Cannot delete the last remaining admin."
PORTFOLIO_NOT_FOUND = "❌ Portfolio not found."
SECURITY_NOT_FOUND = "❌ Security '{}' not found."
INSUFFICIENT_FUNDS = "❌ Insufficient funds. Required: ${:.2f}, Available: ${:.2f}"
INSUFFICIENT_SHARES = "❌ Insufficient shares. You only have {} shares."
NOT_OWNER = "❌ You can only {} your own portfolios."
INVALID_NUMBER = "❌ {} must be a valid number."
POSITIVE_REQUIRED = "❌ {} must be positive."
FIELD_REQUIRED = "❌ {} is required."
NO_DIVIDEND_HOLDINGS = "❌ No dividend-paying holdings in this portfolio."

USER_HEADER = ["Username", "First Name", "Last Name", "Balance", "Role"]
SECURITY_HEADER = ["Ticker", "Name", "Price", "Div Yield", "Sector"]
PORTFOLIO_HEADER = ["ID", "Owner", "Name", "Total Value"]
PERFORMANCE_HEADER = ["Metric", "Value"]
DIVIDEND_HEADER = ["Ticker", "Quantity", "Div Yield", "Est. Annual"]