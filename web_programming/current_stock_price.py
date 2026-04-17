"""
Get the current stock price from Yahoo Finance.

Parses the qsp-price span tag from the Yahoo Finance quote page.
"""

import requests
from bs4 import BeautifulSoup

YAHOO_FINANCE_BASE = "https://finance.yahoo.com/quote"


def build_quote_url(symbol: str) -> str:
    """
    Build the Yahoo Finance quote URL for a given ticker symbol.

    >>> build_quote_url("AAPL")
    'https://finance.yahoo.com/quote/AAPL?p=AAPL'
    >>> build_quote_url("GOOG")
    'https://finance.yahoo.com/quote/GOOG?p=GOOG'
    """
    return f"{YAHOO_FINANCE_BASE}/{symbol}?p={symbol}"


def stock_price(symbol: str = "AAPL") -> str:
    """
    Return the current stock price for the given ticker symbol.

    >>> stock_price("EEEE")  # doctest: +SKIP
    'No <fin-streamer> tag with the specified data-testid attribute found.'
    >>> isinstance(float(stock_price("GOOG")), float)  # doctest: +SKIP
    True
    """
    url = build_quote_url(symbol)
    source = requests.get(
        url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
    ).text
    soup = BeautifulSoup(source, "html.parser")
    tag = soup.find("span", {"data-testid": "qsp-price"})
    if tag:
        return tag.get_text()
    return "No <fin-streamer> tag with the specified data-testid attribute found."


if __name__ == "__main__":
    for symbol in "AAPL AMZN IBM GOOG MSFT ORCL".split():
        print(f"Current {symbol:<4} stock price is {stock_price(symbol):>8}")
