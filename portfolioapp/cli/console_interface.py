from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, FloatPrompt
from rich import print as rprint
import db
from services.user_service import UserService
from services.portfolio_service import PortfolioService
from services.security_service import SecurityService
from services.transaction_service import TransactionService
from services.exceptions import AuthenticationError, AuthorizationError, ValidationError, PortfolioError, InvestmentError
from domain.user import User
from domain.portfolio import Portfolio

class ConsoleInterface:
    """Main console interface for the application"""
    
    def __init__(self):
        self.console = Console()
        self.current_user: Optional[User] = None
    
    def run(self):
        """Main application loop"""
        try:
            while True:
                self.show_login_menu()
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {e}[/red]")
    
    def show_login_menu(self):
        """Display login menu"""
        self.console.clear()
        self.console.rule("[bold blue]Portfolio Manager Login[/bold blue]")
        
        while True:
            try:
                table = Table(show_header=False, box=None)
                table.add_column("", style="cyan")
                table.add_row("1. Login")
                table.add_row("2. Exit")
                self.console.print(table)
                
                choice = Prompt.ask("Select option", choices=["1", "2"])
                
                if choice == "1":
                    if self.handle_login():
                        self.show_main_menu()
                        break
                elif choice == "2":
                    self.console.print("[green]Thank you for using Portfolio Manager![/green]")
                    exit(0)
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def handle_login(self) -> bool:
        """Handle user login"""
        try:
            username = Prompt.ask("Username")
            if not username.strip():
                self.console.print("[red]Username is required[/red]")
                return False
                
            password = Prompt.ask("Password", password=True)
            if not password:
                self.console.print("[red]Password is required[/red]")
                return False
            
            success, user = UserService.authenticate(username, password)
            if success:
                self.current_user = user
                self.console.print(f"[green]Welcome, {user.full_name}![/green]")
                return True
            else:
                self.console.print("[red]Invalid username or password[/red]")
                return False
        except Exception as e:
            self.console.print(f"[red]Login error: {e}[/red]")
            return False
    
    def show_main_menu(self):
        """Display main menu"""
        while self.current_user:
            try:
                self.console.clear()
                self.console.rule(f"[bold blue]Main Menu - Welcome {self.current_user.full_name}[/bold blue]")
                self.console.print(f"[yellow]Balance: ${self.current_user.balance:,.2f}[/yellow]")
                
                table = Table(show_header=False, box=None)
                table.add_column("", style="cyan")
                table.add_row("1. Manage Users")
                table.add_row("2. Manage Portfolios")
                table.add_row("3. Marketplace")
                table.add_row("4. Transaction History")
                table.add_row("5. Logout")
                self.console.print(table)
                
                choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5"])
                
                if choice == "1":
                    self.show_manage_users_menu()
                elif choice == "2":
                    self.show_manage_portfolios_menu()
                elif choice == "3":
                    self.show_marketplace_menu()
                elif choice == "4":
                    self.show_transaction_history()
                elif choice == "5":
                    UserService.logout()
                    self.current_user = None
                    self.console.print("[green]Logged out successfully[/green]")
            except Exception as e:
                self.console.print(f"[red]Error in main menu: {e}[/red]")
                Prompt.ask("Press Enter to continue")
    
    def show_manage_users_menu(self):
        """Display manage users menu (admin only)"""
        if not UserService.is_admin(self.current_user):
            self.console.print("[red]Access denied. Admin privileges required.[/red]")
            Prompt.ask("Press Enter to continue")
            return
        
        while True:
            try:
                self.console.clear()
                self.console.rule("[bold blue]Manage Users[/bold blue]")
                
                table = Table(show_header=False, box=None)
                table.add_column("", style="cyan")
                table.add_row("1. View Users")
                table.add_row("2. Add User")
                table.add_row("3. Delete User")
                table.add_row("4. Back to Main Menu")
                self.console.print(table)
                
                choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"])
                
                if choice == "1":
                    self.show_all_users()
                elif choice == "2":
                    self.handle_add_user()
                elif choice == "3":
                    self.handle_delete_user()
                elif choice == "4":
                    break
            except Exception as e:
                self.console.print(f"[red]Error in manage users menu: {e}[/red]")
                Prompt.ask("Press Enter to continue")
    
    def show_all_users(self):
        """Display all users in a table"""
        try:
            users = UserService.get_all_users()
            
            table = Table(title="All Users", show_header=True, header_style="bold magenta")
            table.add_column("Username", style="cyan")
            table.add_column("Full Name", style="white")
            table.add_column("Balance", justify="right", style="green")
            
            for user in users:
                table.add_row(
                    user.username,
                    user.full_name,
                    f"${user.balance:,.2f}"
                )
            
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error displaying users: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def handle_add_user(self):
        """Handle adding a new user"""
        try:
            self.console.rule("[bold blue]Add New User[/bold blue]")
            
            first_name = Prompt.ask("First Name")
            last_name = Prompt.ask("Last Name")
            username = Prompt.ask("Username")
            password = Prompt.ask("Password", password=True)
            balance = FloatPrompt.ask("Initial Balance")
            
            success, message = UserService.create_user(first_name, last_name, username, password, balance)
            
            if success:
                self.console.print(f"[green]{message}[/green]")
            else:
                self.console.print(f"[red]{message}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error adding user: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def handle_delete_user(self):
        """Handle deleting a user"""
        try:
            self.console.rule("[bold blue]Delete User[/bold blue]")
            
            username = Prompt.ask("Username to delete")
            
            success, message = UserService.delete_user(username)
            
            if success:
                self.console.print(f"[green]{message}[/green]")
            else:
                self.console.print(f"[red]{message}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error deleting user: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def show_manage_portfolios_menu(self):
        """Display manage portfolios menu"""
        while True:
            try:
                self.console.clear()
                self.console.rule("[bold blue]Manage Portfolios[/bold blue]")
                
                table = Table(show_header=False, box=None)
                table.add_column("", style="cyan")
                table.add_row("1. View Portfolios")
                table.add_row("2. Create Portfolio")
                table.add_row("3. Delete Portfolio")
                table.add_row("4. Harvest Investment")
                table.add_row("5. Portfolio Performance")
                table.add_row("6. Portfolio Analytics")
                table.add_row("7. Back to Main Menu")
                self.console.print(table)
                
                choice = Prompt.ask("Select option", choices=["1", "2", "3", "4", "5", "6", "7"])
                
                if choice == "1":
                    self.show_user_portfolios()
                elif choice == "2":
                    self.handle_create_portfolio()
                elif choice == "3":
                    self.handle_delete_portfolio()
                elif choice == "4":
                    self.handle_harvest_investment()
                elif choice == "5":
                    self.show_portfolio_performance()
                elif choice == "6":
                    self.show_portfolio_analytics()
                elif choice == "7":
                    break
            except Exception as e:
                self.console.print(f"[red]Error in manage portfolios menu: {e}[/red]")
                Prompt.ask("Press Enter to continue")
    
    def show_user_portfolios(self):
        
        try:
            portfolios = PortfolioService.get_user_portfolios(self.current_user.username)
            
            if not portfolios:
                self.console.print("[yellow]No portfolios found[/yellow]")
                Prompt.ask("Press Enter to continue")
                return
            
            table = Table(title="Your Portfolios", show_header=True, header_style="bold magenta")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="white")
            table.add_column("Description", style="white")
            table.add_column("Holdings", justify="right", style="yellow")
            table.add_column("Total Value", justify="right", style="green")
            
            for portfolio in portfolios:
                table.add_row(
                    str(portfolio.id),
                    portfolio.name,
                    portfolio.description,
                    str(len(portfolio.holdings)),
                    f"${portfolio.get_total_cost():,.2f}"
                )
            
            self.console.print(table)
            
            # Show holdings for selected portfolio
            if portfolios:
                portfolio_id = IntPrompt.ask("Enter portfolio ID to view holdings (0 to skip)", default=0)
                if portfolio_id > 0:
                    self.show_portfolio_holdings(portfolio_id)
        except Exception as e:
            self.console.print(f"[red]Error displaying portfolios: {e}[/red]")
            Prompt.ask("Press Enter to continue")
    
    def show_portfolio_holdings(self, portfolio_id: int):
        
        try:
            portfolio = db.get_portfolio_by_id(self.current_user.username, portfolio_id)
            if not portfolio:
                self.console.print("[red]Portfolio not found[/red]")
                Prompt.ask("Press Enter to continue")
                return
            
            if not portfolio.holdings:
                self.console.print("[yellow]No investments in this portfolio[/yellow]")
                Prompt.ask("Press Enter to continue")
                return
            
            table = Table(title=f"Holdings for {portfolio.name}", show_header=True, header_style="bold magenta")
            table.add_column("Ticker", style="cyan")
            table.add_column("Quantity", justify="right", style="white")
            table.add_column("Purchase Price", justify="right", style="yellow")
            table.add_column("Total Value", justify="right", style="green")
            
            for investment in portfolio.holdings:
                table.add_row(
                    investment.ticker,
                    str(investment.quantity),
                    f"${investment.purchase_price:,.2f}",
                    f"${investment.total_value:,.2f}"
                )
            
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error displaying portfolio holdings: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def handle_create_portfolio(self):
        """Handle creating a new portfolio"""
        try:
            self.console.rule("[bold blue]Create New Portfolio[/bold blue]")
            
            name = Prompt.ask("Portfolio Name")
            description = Prompt.ask("Portfolio Description")
            
            success, message = PortfolioService.create_portfolio(self.current_user.username, name, description)
            
            if success:
                self.console.print(f"[green]{message}[/green]")
            else:
                self.console.print(f"[red]{message}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error creating portfolio: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def handle_delete_portfolio(self):
        
        try:
            self.console.rule("[bold blue]Delete Portfolio[/bold blue]")
            
            portfolio_id = IntPrompt.ask("Portfolio ID to delete")
            
            success, message = PortfolioService.delete_portfolio(self.current_user.username, portfolio_id)
            
            if success:
                self.console.print(f"[green]{message}[/green]")
            else:
                self.console.print(f"[red]{message}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error deleting portfolio: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def handle_harvest_investment(self):
        """Handle liquidating an investment"""
        try:
            self.console.rule("[bold blue]Harvest Investment[/bold blue]")
            
            portfolio_id = IntPrompt.ask("Portfolio ID")
            portfolio = db.get_portfolio_by_id(self.current_user.username, portfolio_id)
            
            if not portfolio:
                self.console.print("[red]Portfolio not found[/red]")
                Prompt.ask("Press Enter to continue")
                return
            
            if not portfolio.holdings:
                self.console.print("[yellow]No investments in this portfolio[/yellow]")
                Prompt.ask("Press Enter to continue")
                return
            
            # Show current holdings
            self.show_portfolio_holdings(portfolio_id)
            
            ticker = Prompt.ask("Ticker to liquidate").upper()
            quantity = IntPrompt.ask("Quantity to liquidate")
            sale_price = FloatPrompt.ask("Sale price per share")
            
            success, message, proceeds = PortfolioService.liquidate_investment(
                portfolio, ticker, quantity, sale_price
            )
            
            if success:
                # Update user balance
                if self.current_user.update_balance(proceeds):
                    # RECORD TRANSACTION
                    PortfolioService.record_transaction(
                        self.current_user.username, "SELL", ticker, quantity, 
                        sale_price, proceeds, portfolio_id
                    )
                    
                    self.console.print(f"[green]{message}[/green]")
                    self.console.print(f"[green]Sale proceeds: ${proceeds:,.2f}[/green]")
                    self.console.print(f"[green]New balance: ${self.current_user.balance:,.2f}[/green]")
                else:
                    self.console.print("[red]Failed to update balance[/red]")
            else:
                self.console.print(f"[red]{message}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error harvesting investment: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def show_portfolio_performance(self):
        """Display portfolio performance metrics"""
        try:
            portfolios = PortfolioService.get_user_portfolios(self.current_user.username)
            
            if not portfolios:
                self.console.print("[yellow]No portfolios found[/yellow]")
                Prompt.ask("Press Enter to continue")
                return
            
            table = Table(title="Portfolio Performance", show_header=True, header_style="bold magenta")
            table.add_column("Portfolio", style="cyan")
            table.add_column("Cost Basis", justify="right", style="white")
            table.add_column("Current Value", justify="right", style="white")
            table.add_column("Gain/Loss", justify="right", style="white")
            table.add_column("Performance %", justify="right", style="white")
            
            for portfolio in portfolios:
                performance = PortfolioService.get_portfolio_performance(portfolio)
                
                # Color coding for gain/loss
                gain_loss = performance["unrealized_gain_loss"]
                gain_loss_style = "green" if gain_loss >= 0 else "red"
                gain_loss_text = f"${gain_loss:+,.2f}"
                
                # Color coding for performance percentage
                perf_percentage = performance["performance_percentage"]
                perf_style = "green" if perf_percentage >= 0 else "red"
                perf_text = f"{perf_percentage:+.2f}%"
                
                table.add_row(
                    f"{portfolio.name} (ID: {portfolio.id})",
                    f"${performance['total_cost']:,.2f}",
                    f"${performance['current_value']:,.2f}",
                    f"[{gain_loss_style}]{gain_loss_text}[/{gain_loss_style}]",
                    f"[{perf_style}]{perf_text}[/{perf_style}]"
                )
            
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error displaying portfolio performance: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def show_portfolio_analytics(self):
        """Display portfolio analytics and sector breakdown"""
        try:
            portfolio_id = IntPrompt.ask("Enter portfolio ID for analytics", default=0)
            if portfolio_id == 0:
                return
            
            portfolio = db.get_portfolio_by_id(self.current_user.username, portfolio_id)
            if not portfolio:
                self.console.print("[red]Portfolio not found[/red]")
                Prompt.ask("Press Enter to continue")
                return
            
            if not portfolio.holdings:
                self.console.print("[yellow]No investments in this portfolio[/yellow]")
                Prompt.ask("Press Enter to continue")
                return
            
            # Get sector breakdown
            sector_breakdown = PortfolioService.get_portfolio_analytics(portfolio)
            
            table = Table(title=f"Sector Breakdown - {portfolio.name}", 
                         show_header=True, header_style="bold magenta")
            table.add_column("Sector", style="cyan")
            table.add_column("Allocation %", justify="right", style="green")
            
            for sector, allocation in sector_breakdown.items():
                table.add_row(sector, f"{allocation:.1f}%")
            
            self.console.print(table)
            
            # Show holding concentration
            self.console.print("\n[bold]Top Holdings:[/bold]")
            holdings_table = Table(show_header=True, header_style="bold blue")
            holdings_table.add_column("Ticker", style="cyan")
            holdings_table.add_column("Quantity", justify="right", style="white")
            holdings_table.add_column("Value", justify="right", style="green")
            holdings_table.add_column("Weight %", justify="right", style="yellow")
            
            total_value = portfolio.get_total_cost()
            for investment in portfolio.holdings:
                weight = (investment.total_value / total_value) * 100 if total_value > 0 else 0
                holdings_table.add_row(
                    investment.ticker,
                    str(investment.quantity),
                    f"${investment.total_value:,.2f}",
                    f"{weight:.1f}%"
                )
            
            self.console.print(holdings_table)
        except Exception as e:
            self.console.print(f"[red]Error displaying portfolio analytics: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def show_marketplace_menu(self):
        """Display marketplace menu"""
        while True:
            try:
                self.console.clear()
                self.console.rule("[bold blue]Marketplace[/bold blue]")
                
                table = Table(show_header=False, box=None)
                table.add_column("", style="cyan")
                table.add_row("1. View Securities")
                table.add_row("2. Place Buy Order")
                table.add_row("3. Back to Main Menu")
                self.console.print(table)
                
                choice = Prompt.ask("Select option", choices=["1", "2", "3"])
                
                if choice == "1":
                    self.show_all_securities()
                elif choice == "2":
                    self.handle_buy_order()
                elif choice == "3":
                    break
            except Exception as e:
                self.console.print(f"[red]Error in marketplace menu: {e}[/red]")
                Prompt.ask("Press Enter to continue")
    
    def show_all_securities(self):
        """Display all available securities"""
        try:
            securities = SecurityService.get_all_securities()
            
            table = Table(title="Available Securities", show_header=True, header_style="bold magenta")
            table.add_column("Ticker", style="cyan")
            table.add_column("Issuer", style="white")
            table.add_column("Price", justify="right", style="green")
            
            for security in securities:
                table.add_row(
                    security.ticker,
                    security.issuer,
                    f"${security.price:,.2f}"
                )
            
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error displaying securities: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def handle_buy_order(self):
        
        try:
            self.console.rule("[bold blue]Place Buy Order[/bold blue]")
            
            portfolio_id = IntPrompt.ask("Portfolio ID")
            if portfolio_id <= 0:
                self.console.print("[red]Invalid portfolio ID[/red]")
                Prompt.ask("Press Enter to continue")
                return
            
            portfolio = db.get_portfolio_by_id(self.current_user.username, portfolio_id)
            if not portfolio:
                self.console.print("[red]Portfolio not found[/red]")
                Prompt.ask("Press Enter to continue")
                return
            
            ticker = Prompt.ask("Ticker").upper()
            if not ticker.strip():
                self.console.print("[red]Ticker is required[/red]")
                Prompt.ask("Press Enter to continue")
                return
            
            security = SecurityService.get_security(ticker)
            if not security:
                self.console.print("[red]Security not found[/red]")
                Prompt.ask("Press Enter to continue")
                return
            
            quantity = IntPrompt.ask("Quantity")
            if quantity <= 0:
                self.console.print("[red]Quantity must be positive[/red]")
                Prompt.ask("Press Enter to continue")
                return
            
            # Check if user has sufficient balance
            total_cost = SecurityService.calculate_order_amount(ticker, quantity)
            if total_cost is None:
                self.console.print("[red]Failed to calculate order amount[/red]")
                Prompt.ask("Press Enter to continue")
                return
            
            if total_cost > self.current_user.balance:
                self.console.print(f"[red]Insufficient balance. Required: ${total_cost:,.2f}, Available: ${self.current_user.balance:,.2f}[/red]")
                Prompt.ask("Press Enter to continue")
                return
            
            # Process the buy order
            success, message = PortfolioService.add_investment(portfolio, security, quantity)
            
            if success:
                # Deduct from user balance
                if self.current_user.update_balance(-total_cost):
                    # RECORD TRANSACTION
                    PortfolioService.record_transaction(
                        self.current_user.username, "BUY", ticker, quantity, 
                        security.price, total_cost, portfolio_id
                    )
                    
                    self.console.print(f"[green]{message}[/green]")
                    self.console.print(f"[green]Order cost: ${total_cost:,.2f}[/green]")
                    self.console.print(f"[green]New balance: ${self.current_user.balance:,.2f}[/green]")
                else:
                    self.console.print("[red]Failed to update balance[/red]")
            else:
                self.console.print(f"[red]{message}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error placing buy order: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")
    
    def show_transaction_history(self):
        
        try:
            transactions = TransactionService.get_recent_transactions(self.current_user.username, 20)
            
            if not transactions:
                self.console.print("[yellow]No transactions found[/yellow]")
                Prompt.ask("Press Enter to continue")
                return
            
            table = Table(title="Recent Transactions", show_header=True, header_style="bold magenta")
            table.add_column("Date", style="white")
            table.add_column("Type", style="cyan")
            table.add_column("Ticker", style="white")
            table.add_column("Quantity", justify="right", style="white")
            table.add_column("Price", justify="right", style="yellow")
            table.add_column("Amount", justify="right", style="green")
            table.add_column("Portfolio", justify="right", style="white")
            
            for transaction in transactions:
                # Color coding for transaction type
                type_style = "green" if transaction.type == "BUY" else "red"
                type_text = f"[{type_style}]{transaction.type}[/{type_style}]"
                
                table.add_row(
                    transaction.timestamp.strftime("%Y-%m-%d %H:%M"),
                    type_text,
                    transaction.ticker,
                    str(transaction.quantity),
                    f"${transaction.price:,.2f}",
                    f"${transaction.total_amount:,.2f}",
                    str(transaction.portfolio_id)
                )
            
            self.console.print(table)
        except Exception as e:
            self.console.print(f"[red]Error displaying transaction history: {e}[/red]")
        
        Prompt.ask("Press Enter to continue")