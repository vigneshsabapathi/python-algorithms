"""
Emails From URL – three domain extraction approaches + benchmark.

Approach 1: urllib.parse.urlparse (standard library)
Approach 2: regex-based domain extraction
Approach 3: manual string split
"""

import re
import time
from urllib import parse


SAMPLE_URLS = [
    "https://a.b.c.d/e/f?g=h,i=j#k",
    "https://mail.google.com/mail/u/0/",
    "https://api.github.com/repos/TheAlgorithms/Python",
    "Not a URL!",
]


# ---------------------------------------------------------------------------
# Approach 1 – urllib.parse (standard)
# ---------------------------------------------------------------------------
def domain_via_urlparse(url: str) -> str:
    """
    Extract root domain using urllib.parse.urlparse.

    >>> domain_via_urlparse("https://a.b.c.d/e/f?g=h")
    'c.d'
    >>> domain_via_urlparse("https://api.github.com/repos")
    'github.com'
    >>> domain_via_urlparse("Not a URL!")
    ''
    """
    netloc = parse.urlparse(url).netloc
    parts = netloc.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else netloc


# ---------------------------------------------------------------------------
# Approach 2 – regex
# ---------------------------------------------------------------------------
_DOMAIN_RE = re.compile(r"https?://(?:[^./]+\.)*([^./]+\.[^./]+)(?:/|$)")


def domain_via_regex(url: str) -> str:
    """
    Extract root domain using a regex pattern.

    >>> domain_via_regex("https://a.b.c.d/e/f?g=h")
    'c.d'
    >>> domain_via_regex("https://api.github.com/repos")
    'github.com'
    >>> domain_via_regex("Not a URL!")
    ''
    """
    m = _DOMAIN_RE.match(url)
    return m.group(1) if m else ""


# ---------------------------------------------------------------------------
# Approach 3 – manual split (no imports)
# ---------------------------------------------------------------------------
def domain_via_split(url: str) -> str:
    """
    Extract root domain by manually splitting on '/' and '.'.

    >>> domain_via_split("https://a.b.c.d/e/f?g=h")
    'c.d'
    >>> domain_via_split("https://api.github.com/repos")
    'github.com'
    >>> domain_via_split("Not a URL!")
    ''
    """
    try:
        netloc = url.split("//", 1)[1].split("/", 1)[0]
        parts = netloc.split(".")
        return ".".join(parts[-2:]) if len(parts) >= 2 else netloc
    except IndexError:
        return ""


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 100_000) -> None:
    approaches = [
        ("urlparse", domain_via_urlparse),
        ("regex", domain_via_regex),
        ("manual split", domain_via_split),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            for url in SAMPLE_URLS:
                fn(url)
        elapsed = time.perf_counter() - t0
        per_call = elapsed / (runs * len(SAMPLE_URLS)) * 1e6
        print(f"{name:15s}: {runs*len(SAMPLE_URLS)} calls in {elapsed:.4f}s ({per_call:.3f} µs/call)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
