from sqlalchemy import select
from portfolioapp.database import get_session
from portfolioapp.domain.security import Security
from rich.table import Table
import portfolioapp.database as database


def get_all_securities():
    try:
        session = database.get_session()
        return session.execute(select(Security)).scalars().all()
    except Exception as e:
        return []
    finally:
        session.close() if 'session' in locals() else None


def build_securities_table(securities):
    table = Table(title="Securities")
    table.add_column("Ticker", style="cyan")
    table.add_column("Issuer", style="white")
    table.add_column("Price", justify="right", style="green")

    for s in securities:
        table.add_row(s.ticker, s.issuer, f"${s.price:.2f}")

    return table
