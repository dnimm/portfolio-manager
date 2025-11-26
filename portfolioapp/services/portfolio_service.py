from sqlalchemy import select
from portfolioapp.database import get_session
from portfolioapp.cli.input_collector import collect_inputs
from portfolioapp.domain.portfolio import Portfolio
from portfolioapp.domain.user import User
from portfolioapp.domain.security import Security
from portfolioapp.domain.investment import Investment
from portfolioapp.services.transaction_service import record_transaction
import portfolioapp.database as database


def get_all_portfolios():
    try:
        session = database.get_session()
        ports = session.execute(select(Portfolio)).scalars().all()
        return ports
    except Exception:
        return []
    finally:
        session.close() if 'session' in locals() else None


def build_portfolio_table(portfolios):
    from rich.table import Table
    table = Table(title="Portfolios")
    table.add_column("ID", style="cyan")
    table.add_column("Name")
    table.add_column("Owner")
    table.add_column("Description")

    for p in portfolios:
        table.add_row(str(p.id), p.name, p.owner_username, p.description)

    return table


def create_portfolio():
    try:
        inputs = collect_inputs({
            "Portfolio Name": "name",
            "Owner Username": "owner",
            "Description": "desc"
        })

        session = get_session()

        owner = session.get(User, inputs["owner"])
        if not owner:
            return "User not found."

        p = Portfolio(
            name=inputs["name"],
            owner_username=inputs["owner"],
            description=inputs["desc"]
        )

        session.add(p)
        session.commit()
        return "Portfolio created."

    except Exception as e:
        return f"Error creating portfolio: {str(e)}"

    finally:
        session.close() if 'session' in locals() else None



def delete_portfolio():
    try:
        inp = collect_inputs({"Portfolio ID": "pid"})
        pid = int(inp["pid"])

        session = get_session()
        port = session.get(Portfolio, pid)

        if not port:
            return "Portfolio not found."

        if len(port.investments) > 0:
            return "Portfolio contains holdings. Sell them first."

        session.delete(port)
        session.commit()
        return "Portfolio deleted."

    except Exception as e:
        return f"Error deleting portfolio: {str(e)}"

    finally:
        session.close() if 'session' in locals() else None



def buy_security():
    try:
        inputs = collect_inputs({
            "Portfolio ID": "pid",
            "Ticker": "ticker",
            "Quantity": "qty"
        })

        pid = int(inputs["pid"])
        ticker = inputs["ticker"]
        qty = int(inputs["qty"])

        session = get_session()
        port = session.get(Portfolio, pid)

        if not port:
            return "Invalid portfolio ID."

        sec = session.execute(
            select(Security).where(Security.ticker == ticker)
        ).scalar_one_or_none()

        if not sec:
            return "Invalid ticker."

        total_cost = sec.price * qty
        user = port.user

        if user.balance < total_cost:
            return "Insufficient balance."

        user.balance -= total_cost

        inv = None
        for i in port.investments:
            if i.ticker == ticker:
                inv = i
                break

        if inv:
            inv.quantity += qty
        else:
            new_inv = Investment(
                portfolio_id=pid,
                ticker=ticker,
                quantity=qty,
                purchase_price=sec.price
            )
            session.add(new_inv)

        session.commit()
        record_transaction(pid, ticker, "BUY", qty, sec.price)

        return "Purchase completed."

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        session.close() if 'session' in locals() else None



def sell_security():
    try:
        inputs = collect_inputs({
            "Portfolio ID": "pid",
            "Ticker": "ticker",
            "Quantity": "qty",
            "Sale Price": "price"
        })

        pid = int(inputs["pid"])
        ticker = inputs["ticker"]
        qty = int(inputs["qty"])
        price = float(inputs["price"])

        session = get_session()
        port = session.get(Portfolio, pid)

        if not port:
            return "Invalid portfolio."

        inv = None
        for i in port.investments:
            if i.ticker == ticker:
                inv = i
                break

        if not inv:
            return "Investment not found."

        if qty > inv.quantity:
            return "Not enough shares."

        proceeds = qty * price
        user = port.user
        user.balance += proceeds

        if qty == inv.quantity:
            session.delete(inv)
        else:
            inv.quantity -= qty

        session.commit()
        record_transaction(pid, ticker, "SELL", qty, price)

        return "Sale completed."

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        session.close() if 'session' in locals() else None
