"""
Look up book and author data from Open Library using ISBN or OLID.

API docs: https://openlibrary.org/developers/api
"""

from json import JSONDecodeError

import requests

OPENLIBRARY_BASE = "https://openlibrary.org"


def build_openlibrary_url(olid: str) -> str:
    """
    Build the Open Library JSON endpoint URL for a given OLID or ISBN path.

    >>> build_openlibrary_url("isbn/0140328726")
    'https://openlibrary.org/isbn/0140328726.json'
    >>> build_openlibrary_url("/authors/OL34184A")
    'https://openlibrary.org/authors/OL34184A.json'
    """
    clean = olid.strip().strip("/")
    return f"{OPENLIBRARY_BASE}/{clean}.json"


def validate_olid(olid: str) -> str:
    """
    Strip and validate an OLID, returning the cleaned form (no leading slash).

    Raises ValueError if the path has wrong number of segments.

    >>> validate_olid("isbn/0140328726")
    'isbn/0140328726'
    >>> validate_olid("/authors/OL34184A")
    'authors/OL34184A'
    >>> validate_olid("bad")
    Traceback (most recent call last):
        ...
    ValueError: bad is not a valid Open Library olid
    """
    clean = olid.strip().strip("/")
    if clean.count("/") != 1:
        raise ValueError(f"{olid} is not a valid Open Library olid")
    return clean


def get_openlibrary_data(olid: str = "isbn/0140328726") -> dict:
    """
    Return Open Library data for an OLID or ISBN path as a Python dict.

    >>> get_openlibrary_data("isbn/0140328726")  # doctest: +SKIP
    {'publishers': ['Puffin'], 'number_of_pages': 96, ...}
    """
    clean = validate_olid(olid)
    return requests.get(
        f"{OPENLIBRARY_BASE}/{clean}.json", timeout=10, allow_redirects=True
    ).json()


def summarize_book(ol_book_data: dict) -> dict:
    """
    Extract a summary dict from Open Library book data.

    >>> data = {"title": "Matilda", "publish_date": "1988", "authors": [{"key": "/authors/OL34184A"}], "number_of_pages": 240, "isbn_10": ["0140328726"], "isbn_13": ["9780140328721"]}
    >>> summarize_book(data)  # doctest: +SKIP
    {'Title': 'Matilda', 'Publish date': '1988', ...}
    """
    desired_keys = {
        "title": "Title",
        "publish_date": "Publish date",
        "authors": "Authors",
        "number_of_pages": "Number of pages",
        "isbn_10": "ISBN (10)",
        "isbn_13": "ISBN (13)",
    }
    result = {
        better_key: ol_book_data[key]
        for key, better_key in desired_keys.items()
        if key in ol_book_data
    }
    result["Authors"] = [
        get_openlibrary_data(author["key"])["name"]
        for author in result.get("Authors", [])
    ]
    for key, value in result.items():
        if isinstance(value, list):
            result[key] = ", ".join(str(v) for v in value)
    return result


if __name__ == "__main__":
    while True:
        isbn = input("\nEnter ISBN (10 or 13 digits) or 'quit': ").strip()
        if isbn.lower() in ("", "q", "quit", "exit", "stop"):
            break
        if len(isbn) not in (10, 13) or not isbn.isdigit():
            print(f"Sorry, '{isbn}' is not a valid ISBN.")
            continue
        print(f"\nSearching Open Library for ISBN: {isbn}...")
        try:
            summary = summarize_book(get_openlibrary_data(f"isbn/{isbn}"))
            print("\n".join(f"{k}: {v}" for k, v in summary.items()))
        except JSONDecodeError:
            print(f"Sorry, no results found for ISBN: {isbn}.")
