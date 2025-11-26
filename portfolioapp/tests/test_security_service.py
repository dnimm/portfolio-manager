import pytest
from portfolioapp.domain.security import Security
from portfolioapp.services.security_service import (
    get_all_securities, build_securities_table
)
import portfolioapp.database as database
from rich.table import Table


def test_add_security(db_session):

    database.get_session = lambda: db_session

    s = Security(ticker="AAA", issuer="Corp", price=1000)
    db_session.add(s)
    db_session.commit()

    results = get_all_securities()
    assert any(sec.ticker == "AAA" for sec in results)


def test_get_all_securities_empty(db_session):
    database.get_session = lambda: db_session

    db_session.query(Security).delete()
    db_session.commit()

    results = get_all_securities()
    assert isinstance(results, list)
    assert results == []



def test_get_all_securities_exception(monkeypatch):
    
    def bad_session():
        raise OperationalError("Bad DB", None, None)

    monkeypatch.setattr(database, "get_session", bad_session)

    results = get_all_securities()

    assert results == []






def test_build_securities_table_populated():
    securities = [
        Security(ticker="XYZ", issuer="XYZ Corp", price=50.0),
        Security(ticker="LMN", issuer="LMN Corp", price=75.5)
    ]

    table = build_securities_table(securities)
    assert isinstance(table, Table)

   
    assert table.row_count == 2







