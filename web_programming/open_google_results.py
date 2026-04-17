"""
Google a query and open the first result in the default web browser.

Parses the first anchor from the Google results HTML.
"""

import webbrowser
from urllib.parse import parse_qs, quote

import requests
from bs4 import BeautifulSoup


def build_google_url(query: str) -> str:
    """
    Build a Google search URL for the given query.

    >>> build_google_url("python algorithms")
    'https://www.google.com/search?q=python%20algorithms&num=100'
    >>> build_google_url("hello world")
    'https://www.google.com/search?q=hello%20world&num=100'
    """
    return f"https://www.google.com/search?q={quote(query)}&num=100"


def open_google_results(query: str) -> str:
    """
    Google a query and open the first result URL in the browser.

    Returns the URL that was opened.

    >>> open_google_results("python")  # doctest: +SKIP
    'https://www.python.org/'
    """
    url = build_google_url(query)
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    try:
        link = soup.find("div").find("a").get("href")
    except AttributeError:
        link = parse_qs(
            soup.find("div").find("a").get("href")
        ).get("url", [""])[0]
    webbrowser.open(link)
    return link


if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Search: ")
    print("Googling.....")
    result = open_google_results(query)
    print(f"Opened: {result}")
