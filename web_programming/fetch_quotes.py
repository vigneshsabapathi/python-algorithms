"""
Fetch inspirational quotes from the ZenQuotes API (no API key required).

API docs: https://zenquotes.io/
Response schema: [{"q": "quote text", "a": "author", "h": "<html>"}]
"""

import pprint

import requests

API_ENDPOINT_URL = "https://zenquotes.io/api"


def quote_of_the_day() -> list:
    """
    Return today's quote of the day from ZenQuotes.

    >>> isinstance(quote_of_the_day(), list)  # doctest: +SKIP
    True
    """
    return requests.get(API_ENDPOINT_URL + "/today", timeout=10).json()


def random_quotes() -> list:
    """
    Return a random quote from ZenQuotes.

    >>> data = random_quotes()  # doctest: +SKIP
    >>> isinstance(data[0]['q'], str)  # doctest: +SKIP
    True
    """
    return requests.get(API_ENDPOINT_URL + "/random", timeout=10).json()


def parse_quote(quote_obj: dict) -> tuple[str, str]:
    """
    Extract the quote text and author from a ZenQuotes response object.

    >>> parse_quote({"q": "Be yourself.", "a": "Oscar Wilde", "h": "<p>...</p>"})
    ('Be yourself.', 'Oscar Wilde')
    >>> parse_quote({"q": "Live simply.", "a": "Gandhi", "h": ""})
    ('Live simply.', 'Gandhi')
    """
    return quote_obj["q"], quote_obj["a"]


if __name__ == "__main__":
    response = random_quotes()
    pprint.pprint(response)
    if response:
        text, author = parse_quote(response[0])
        print(f"\n\"{text}\"\n  — {author}")
