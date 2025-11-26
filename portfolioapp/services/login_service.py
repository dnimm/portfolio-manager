from rich.console import Console
from sqlalchemy import select
from portfolioapp.database import get_session
from portfolioapp.domain.user import User
import portfolioapp.session_state as session_state
import portfolioapp.database as database

_console = Console()

def login():
    try:
        session = database.get_session()
        username = _console.input("Username: ")
        password = _console.input("Password: ")

        user = session.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()

        if user and user.password == password:
            session_state.set_logged_in_user(user)
            _console.print(f"[green]Welcome {user.firstname}![/green]")
        else:
            _console.print("[red]Invalid username or password[/red]")
    except Exception as e:
        _console.print(f"[red]Login error: {str(e)}[/red]")
    finally:
        session.close() if 'session' in locals() else None


def logout():
    session_state.clear_logged_in_user()
    _console.print("[yellow]Logged out[/yellow]")
