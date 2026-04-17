"""
Currency Converter – three URL-building approaches + benchmark.

Approach 1: urllib.parse.urlencode (standard library)
Approach 2: requests.PreparedRequest (library-assisted)
Approach 3: f-string manual build
"""

import time
from urllib.parse import urlencode


SAMPLE_PARAMS = {"from": "USD", "to": "INR", "amount": 100.0, "api_key": "testkey"}
BASE_URL = "https://www.amdoren.com/api/currency.php"


# ---------------------------------------------------------------------------
# Approach 1 – urlencode (standard)
# ---------------------------------------------------------------------------
def build_url_urlencode(base: str, params: dict) -> str:
    """
    Build query URL using urllib.parse.urlencode.

    >>> build_url_urlencode("https://api.example.com/v1", {"a": 1, "b": "x"})
    'https://api.example.com/v1?a=1&b=x'
    """
    return f"{base}?{urlencode(params)}"


# ---------------------------------------------------------------------------
# Approach 2 – requests PreparedRequest
# ---------------------------------------------------------------------------
def build_url_requests(base: str, params: dict) -> str:
    """
    Build query URL using requests.Request().prepare().

    >>> build_url_requests("https://api.example.com/v1", {"a": 1, "b": "x"})
    'https://api.example.com/v1?a=1&b=x'
    """
    import requests

    req = requests.Request("GET", base, params=params)
    return req.prepare().url


# ---------------------------------------------------------------------------
# Approach 3 – manual f-string
# ---------------------------------------------------------------------------
def build_url_manual(base: str, params: dict) -> str:
    """
    Build query URL by joining key=value pairs manually.

    >>> build_url_manual("https://api.example.com/v1", {"a": 1, "b": "x"})
    'https://api.example.com/v1?a=1&b=x'
    """
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{base}?{query}"


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 200_000) -> None:
    approaches = [
        ("urlencode", build_url_urlencode),
        ("requests", build_url_requests),
        ("manual", build_url_manual),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(BASE_URL, SAMPLE_PARAMS)
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.2f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
