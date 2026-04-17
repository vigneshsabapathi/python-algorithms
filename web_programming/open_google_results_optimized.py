"""
Open Google Results – three search URL approaches + benchmark.

Approach 1: f-string + urllib.parse.quote (original)
Approach 2: urllib.parse.urlencode
Approach 3: requests.Request.prepare()
"""

import time
from urllib.parse import quote, urlencode

GOOGLE_BASE = "https://www.google.com/search"


# ---------------------------------------------------------------------------
# Approach 1 – f-string + quote
# ---------------------------------------------------------------------------
def build_google_url_fstring(query: str) -> str:
    """
    Build a Google search URL using f-string and quote.

    >>> build_google_url_fstring("python")
    'https://www.google.com/search?q=python&num=100'
    >>> build_google_url_fstring("hello world")
    'https://www.google.com/search?q=hello%20world&num=100'
    """
    return f"{GOOGLE_BASE}?q={quote(query)}&num=100"


# ---------------------------------------------------------------------------
# Approach 2 – urlencode
# ---------------------------------------------------------------------------
def build_google_url_urlencode(query: str) -> str:
    """
    Build a Google search URL using urlencode.

    >>> build_google_url_urlencode("python")
    'https://www.google.com/search?q=python&num=100'
    """
    return f"{GOOGLE_BASE}?{urlencode({'q': query, 'num': 100})}"


# ---------------------------------------------------------------------------
# Approach 3 – requests PreparedRequest
# ---------------------------------------------------------------------------
def build_google_url_prepared(query: str) -> str:
    """
    Build a Google search URL using requests.Request.prepare().

    >>> build_google_url_prepared("python")
    'https://www.google.com/search?q=python&num=100'
    """
    import requests

    req = requests.Request("GET", GOOGLE_BASE, params={"q": query, "num": 100})
    return req.prepare().url


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 200_000) -> None:
    query = "python interview questions"
    approaches = [
        ("f-string+quote", build_google_url_fstring),
        ("urlencode", build_google_url_urlencode),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(query)
        elapsed = time.perf_counter() - t0
        print(f"{name:18s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")

    runs_small = 5000
    t0 = time.perf_counter()
    for _ in range(runs_small):
        build_google_url_prepared(query)
    elapsed = time.perf_counter() - t0
    print(f"{'requests prep':18s}: {runs_small} runs in {elapsed:.4f}s ({elapsed/runs_small*1e6:.2f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
