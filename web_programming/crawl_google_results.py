"""
Crawl Google search results and open the top links in a browser.

Requires: requests, beautifulsoup4
Note: Google frequently changes its HTML structure; CSS selectors may drift.
"""

import webbrowser

import requests
from bs4 import BeautifulSoup


def build_search_url(query: str) -> str:
    """
    Build a Google search URL from a query string.

    >>> build_search_url("python algorithms")
    'https://www.google.com/search?q=python algorithms'
    >>> build_search_url("")
    'https://www.google.com/search?q='
    """
    return f"https://www.google.com/search?q={query}"


def crawl_google_results(query: str, open_browser: bool = True) -> list[str]:
    """
    Search Google and return/open the top result URLs.

    >>> crawl_google_results("python", open_browser=False)  # doctest: +SKIP
    [...]
    """
    url = build_search_url(query)
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")
    links = list(soup.select(".eZt8xd"))[:5]

    urls = []
    for link in links:
        href = link.get("href", "")
        if link.text == "Maps":
            full_url = href
        else:
            full_url = f"https://google.com{href}"
        urls.append(full_url)
        if open_browser:
            webbrowser.open(full_url)
    return urls


if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Search: ")
    print("Googling.....")
    results = crawl_google_results(query, open_browser=True)
    print(f"Opened {len(results)} results.")
