"""
Search Books by ISBN – three OLID validation and URL-building approaches + benchmark.

Approach 1: string strip + split count (original)
Approach 2: regex validation
Approach 3: pathlib-based URL building
"""

import re
import time
from urllib.parse import urljoin

OPENLIBRARY_BASE = "https://openlibrary.org/"

SAMPLE_OLIDS = [
    "isbn/0140328726",
    "/authors/OL34184A",
    "bad",
    "too/many/slashes",
    "  isbn/0140328726  ",
]


# ---------------------------------------------------------------------------
# Approach 1 – strip + count (original)
# ---------------------------------------------------------------------------
def validate_and_build_url_strip(olid: str) -> str:
    """
    Validate OLID via strip+count and build the Open Library JSON URL.

    >>> validate_and_build_url_strip("isbn/0140328726")
    'https://openlibrary.org/isbn/0140328726.json'
    >>> validate_and_build_url_strip("/authors/OL34184A")
    'https://openlibrary.org/authors/OL34184A.json'
    >>> validate_and_build_url_strip("bad")
    Traceback (most recent call last):
        ...
    ValueError: bad is not a valid Open Library olid
    """
    clean = olid.strip().strip("/")
    if clean.count("/") != 1:
        raise ValueError(f"{olid} is not a valid Open Library olid")
    return f"{OPENLIBRARY_BASE}{clean}.json"


# ---------------------------------------------------------------------------
# Approach 2 – regex validation
# ---------------------------------------------------------------------------
_OLID_RE = re.compile(r"^[a-zA-Z0-9_]+/[a-zA-Z0-9_]+$")


def validate_and_build_url_regex(olid: str) -> str:
    """
    Validate OLID via regex and build the Open Library JSON URL.

    >>> validate_and_build_url_regex("isbn/0140328726")
    'https://openlibrary.org/isbn/0140328726.json'
    >>> validate_and_build_url_regex("authors/OL34184A")
    'https://openlibrary.org/authors/OL34184A.json'
    >>> validate_and_build_url_regex("bad")
    Traceback (most recent call last):
        ...
    ValueError: bad is not a valid Open Library olid
    """
    clean = olid.strip().strip("/")
    if not _OLID_RE.match(clean):
        raise ValueError(f"{olid} is not a valid Open Library olid")
    return f"{OPENLIBRARY_BASE}{clean}.json"


# ---------------------------------------------------------------------------
# Approach 3 – urljoin
# ---------------------------------------------------------------------------
def validate_and_build_url_urljoin(olid: str) -> str:
    """
    Build the Open Library URL using urljoin for safe path joining.

    >>> validate_and_build_url_urljoin("isbn/0140328726")
    'https://openlibrary.org/isbn/0140328726.json'
    >>> validate_and_build_url_urljoin("bad")
    Traceback (most recent call last):
        ...
    ValueError: bad is not a valid Open Library olid
    """
    clean = olid.strip().strip("/")
    if clean.count("/") != 1:
        raise ValueError(f"{olid} is not a valid Open Library olid")
    return urljoin(OPENLIBRARY_BASE, f"{clean}.json")


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 200_000) -> None:
    valid_olid = "isbn/0140328726"
    approaches = [
        ("strip+count", validate_and_build_url_strip),
        ("regex", validate_and_build_url_regex),
        ("urljoin", validate_and_build_url_urljoin),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(valid_olid)
        elapsed = time.perf_counter() - t0
        print(f"{name:15s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
