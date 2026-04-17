"""
Search for GIFs via the Giphy API and return their URLs.

Get an API key at https://developers.giphy.com/dashboard/
"""

import requests

GIPHY_SEARCH_URL = "https://api.giphy.com/v1/gifs/search"


def build_giphy_query(query: str) -> str:
    """
    Format a query string for Giphy by replacing spaces with '+'.

    >>> build_giphy_query("space ship")
    'space+ship'
    >>> build_giphy_query("cat")
    'cat'
    >>> build_giphy_query("happy new year")
    'happy+new+year'
    """
    return "+".join(query.split())


def get_gifs(query: str, api_key: str = "") -> list:
    """
    Return a list of GIF URLs matching the search query.

    >>> get_gifs("cats", "")  # doctest: +SKIP
    ['https://giphy.com/gifs/...', ...]
    """
    formatted_query = build_giphy_query(query)
    url = f"{GIPHY_SEARCH_URL}?q={formatted_query}&api_key={api_key}"
    gifs = requests.get(url, timeout=10).json()["data"]
    return [gif["url"] for gif in gifs]


if __name__ == "__main__":
    import os

    api_key = os.getenv("GIPHY_API_KEY", "YOUR API KEY")
    print("\n".join(get_gifs("space ship", api_key)))
