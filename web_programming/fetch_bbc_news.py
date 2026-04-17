"""
Fetch top BBC News headlines via the NewsAPI.

Get your API key at https://newsapi.org/
Set BBC_NEWS_API_KEY environment variable before use.
"""

import os

import requests

NEWS_API_URL = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey="


def fetch_bbc_news(bbc_news_api_key: str) -> list[str]:
    """
    Return a list of BBC News article titles using the given API key.

    >>> fetch_bbc_news("invalid_key")  # doctest: +SKIP
    []
    """
    bbc_news_page = requests.get(NEWS_API_URL + bbc_news_api_key, timeout=10).json()
    titles = []
    for i, article in enumerate(bbc_news_page.get("articles", []), 1):
        print(f"{i}.) {article['title']}")
        titles.append(article["title"])
    return titles


if __name__ == "__main__":
    api_key = os.getenv("BBC_NEWS_API_KEY", "")
    if not api_key:
        raise KeyError("Set BBC_NEWS_API_KEY environment variable first.")
    fetch_bbc_news(api_key)
