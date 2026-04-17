"""
IP Geolocation – three URL-building and response-parsing approaches + benchmark.

Approach 1: f-string URL + dict key access
Approach 2: urllib.parse.urljoin
Approach 3: format string template
"""

import time
from urllib.parse import urljoin

IPINFO_BASE = "https://ipinfo.io/"


# ---------------------------------------------------------------------------
# Approach 1 – f-string
# ---------------------------------------------------------------------------
def build_url_fstring(ip: str) -> str:
    """
    Build ipinfo URL using an f-string.

    >>> build_url_fstring("8.8.8.8")
    'https://ipinfo.io/8.8.8.8/json'
    """
    return f"https://ipinfo.io/{ip}/json"


# ---------------------------------------------------------------------------
# Approach 2 – urljoin
# ---------------------------------------------------------------------------
def build_url_urljoin(ip: str) -> str:
    """
    Build ipinfo URL using urllib.parse.urljoin.

    >>> build_url_urljoin("8.8.8.8")
    'https://ipinfo.io/8.8.8.8/json'
    """
    return urljoin(IPINFO_BASE, f"{ip}/json")


# ---------------------------------------------------------------------------
# Approach 3 – str.format template
# ---------------------------------------------------------------------------
_URL_TEMPLATE = "https://ipinfo.io/{ip}/json"


def build_url_format(ip: str) -> str:
    """
    Build ipinfo URL using str.format().

    >>> build_url_format("1.1.1.1")
    'https://ipinfo.io/1.1.1.1/json'
    """
    return _URL_TEMPLATE.format(ip=ip)


# ---------------------------------------------------------------------------
# Parse response dict (offline helper)
# ---------------------------------------------------------------------------
def format_location(data: dict) -> str:
    """
    Format a location string from an ipinfo response dict.

    >>> format_location({"city": "Mountain View", "region": "California", "country": "US"})
    'Location: Mountain View, California, US'
    >>> format_location({"ip": "8.8.8.8"})
    'Location data not found.'
    """
    if "city" in data and "region" in data and "country" in data:
        return f"Location: {data['city']}, {data['region']}, {data['country']}"
    return "Location data not found."


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    ip = "8.8.8.8"
    approaches = [
        ("f-string", build_url_fstring),
        ("urljoin", build_url_urljoin),
        ("str.format", build_url_format),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(ip)
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
