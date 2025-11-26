import sys
from rich.console import Console
from rich.table import Table
from portfolioapp.cli import constants
from portfolioapp.services.login_service import login, logout
from portfolioapp.services.user_service import get_all_users, create_user, delete_user, build_users_table
from portfolioapp.services.portfolio_service import get_all_portfolios, build_portfolio_table, create_portfolio, delete_portfolio, sell_security, buy_security
from portfolioapp.services.security_service import get_all_securities, build_securities_table
from portfolioapp.database import get_session
from portfolioapp.domain.transaction import Transaction


_console = Console()

_menus = {
    constants.LOGIN_MENU: """
---- Login ----
1. Login
0. Exit
""",

    constants.MAIN_MENU: """
---- Main Menu ----
1. Manage Users
2. Manage Portfolios
3. Marketplace
4. Logout
5. View Transactions
""",

    constants.MANAGE_USERS_MENU: """
---- Manage Users ----
1. View Users
2. Add User
3. Delete User
0. Back
""",

    constants.MANAGE_PORTFOLIOS_MENU: """
---- Manage Portfolios ----
1. View Portfolios
2. Create Portfolio
3. Delete Portfolio
4. Sell Investment
5. Buy Security
0. Back
""",

    constants.MARKETPLACE_MENU: """
---- Marketplace ----
1. View Securities
0. Back
"""
}


def print_menu(menu_id: int):
   
    try:
        _console.print(_menus[menu_id])
        selection = int(_console.input(">> "))
        handle_user_selection(menu_id, selection)
    except ValueError:
        _console.print("[red]Invalid input. Try again.[/red]")
        print_menu(menu_id)
    except KeyError:
        _console.print("[red]Menu not found.[/red]")
        print_menu(constants.LOGIN_MENU)


def handle_user_selection(menu_id: int, user_selection: int):


    
    if user_selection == 0:
        if menu_id == constants.LOGIN_MENU:
            sys.exit(0)
        elif menu_id == constants.MAIN_MENU:
            logout()
            print_menu(constants.LOGIN_MENU)
        else:
            print_menu(constants.MAIN_MENU)
        return

    try:

       
        if menu_id == constants.LOGIN_MENU and user_selection == 1:
            login()
            print_menu(constants.MAIN_MENU)

        
        elif menu_id == constants.MAIN_MENU:
            if user_selection == 1:
                print_menu(constants.MANAGE_USERS_MENU)
            elif user_selection == 2:
                print_menu(constants.MANAGE_PORTFOLIOS_MENU)
            elif user_selection == 3:
                print_menu(constants.MARKETPLACE_MENU)
            elif user_selection == 4:
                logout()
                print_menu(constants.LOGIN_MENU)
            elif user_selection == 5:
                view_transactions()
                print_menu(constants.MAIN_MENU)

        
        elif menu_id == constants.MANAGE_USERS_MENU:
            if user_selection == 1:
                users = get_all_users()
                table = build_users_table(users)
                _console.print(table)
                print_menu(constants.MANAGE_USERS_MENU)

            elif user_selection == 2:
                result = create_user()
                _console.print(result)
                print_menu(constants.MANAGE_USERS_MENU)

            elif user_selection == 3:
                result = delete_user()
                _console.print(result)
                print_menu(constants.MANAGE_USERS_MENU)

        
        elif menu_id == constants.MANAGE_PORTFOLIOS_MENU:
            if user_selection == 1:
                ports = get_all_portfolios()
                t = build_portfolio_table(ports)
                _console.print(t)
                print_menu(constants.MANAGE_PORTFOLIOS_MENU)

            elif user_selection == 2:
                result = create_portfolio()
                _console.print(result)
                print_menu(constants.MANAGE_PORTFOLIOS_MENU)

            elif user_selection == 3:
                result = delete_portfolio()
                _console.print(result)
                print_menu(constants.MANAGE_PORTFOLIOS_MENU)

            elif user_selection == 4:
                result = sell_security()
                _console.print(result)
                print_menu(constants.MANAGE_PORTFOLIOS_MENU)

            elif user_selection == 5:
                result = buy_security()
                _console.print(result)
                print_menu(constants.MANAGE_PORTFOLIOS_MENU)

        
        elif menu_id == constants.MARKETPLACE_MENU:
            if user_selection == 1:
                secs = get_all_securities()
                t = build_securities_table(secs)
                _console.print(t)
                print_menu(constants.MARKETPLACE_MENU)

    except Exception as e:
        _console.print(f"[red]Error: {str(e)}[/red]")
        print_menu(menu_id)
        
def view_transactions():
    
    try:
        session = get_session()
        txns = session.query(Transaction).all()

        if not txns:
            _console.print("[yellow]No transactions recorded yet.[/yellow]")
            return

        table = Table(title="Transaction History")
        table.add_column("Timestamp")
        table.add_column("Type")
        table.add_column("Ticker")
        table.add_column("Qty")
        table.add_column("Price")
        table.add_column("Portfolio")

        for t in txns:
            table.add_row(
                str(t.timestamp),
                t.txn_type,
                t.ticker,
                str(t.quantity),
                str(t.price),
                str(t.portfolio_id)
            )

        _console.print(table)

    except Exception as e:
        _console.print(f"[red]Error viewing transactions: {str(e)}[/red]")

    finally:
        try:
            session.close()
        except:
            pass