from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import requests
from flask import current_app

from app.cache import cache


@dataclass
class SecurityQuote:
    ticker: str
    date: str
    price: float
    issuer: str


def _get_api_key() -> str:
    api_key = current_app.config.get("ALPHAVANTAGE_API_KEY")
    if not api_key:
        raise ValueError("ALPHAVANTAGE_API_KEY is not configured")
    return api_key


def get_company_name(ticker: str) -> Optional[str]:
    ticker = ticker.upper().strip()
    cache_key = f"company_name:{ticker}"

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    api_key = _get_api_key()
    url = "https://www.alphavantage.co/query"
    params = {"function": "OVERVIEW", "symbol": ticker, "apikey": api_key}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()

    data = resp.json() or {}
    print("COMPANY DATA:", data)
    name = data.get("Name")

    
    if name:
        cache.set(cache_key, name)
        return name

    return None


def get_price_data(ticker: str) -> Optional[dict]:
    ticker = ticker.upper().strip()
    cache_key = f"price_data:{ticker}"

    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    api_key = _get_api_key()
    url = "https://www.alphavantage.co/query"
    params = {"function": "TIME_SERIES_DAILY", "symbol": ticker, "apikey": api_key}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()

    data = resp.json() or {}
    print("PRICE DATA:", data)
    series = data.get("Time Series (Daily)")
    if not series:
        return None

    latest_date = sorted(series.keys(), reverse=True)[0]
    latest = series[latest_date] or {}

    result = {
        "date": latest_date,
        "open": float(latest.get("1. open", 0)),
        "high": float(latest.get("2. high", 0)),
        "low": float(latest.get("3. low", 0)),
        "close": float(latest.get("4. close", 0)),
        "volume": float(latest.get("5. volume", 0)),
    }

    
    cache.set(cache_key, result)
    return result


def get_quote(ticker: str) -> Optional[SecurityQuote]:
    issuer = get_company_name(ticker)
    price_data = get_price_data(ticker)

    if not issuer or not price_data:
        return None

    return SecurityQuote(
        ticker=ticker.upper().strip(),
        issuer=issuer,
        date=price_data["date"],
        price=price_data["close"],
    )