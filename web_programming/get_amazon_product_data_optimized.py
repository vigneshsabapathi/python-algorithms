"""
Amazon Product Data – three price-parsing approaches + benchmark.

Approach 1: direct .text strip (original)
Approach 2: try/except with AttributeError guard
Approach 3: .get_text() with strip and replace pipeline
"""

import time

SAMPLE_PRICE_STRINGS = [
    "₹1,299",
    "₹45,000",
    "₹899.99",
    "",
    "N/A",
]


# ---------------------------------------------------------------------------
# Approach 1 – strip and replace chain (original)
# ---------------------------------------------------------------------------
def clean_price_strip(price_str: str) -> float | None:
    """
    Convert a price string like '₹1,299' to a float.

    >>> clean_price_strip("₹1,299")
    1299.0
    >>> clean_price_strip("₹45,000")
    45000.0
    >>> clean_price_strip("") is None
    True
    """
    try:
        return float(price_str.strip("₹").replace(",", ""))
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Approach 2 – lstrip + translate (faster for large strings)
# ---------------------------------------------------------------------------
_REMOVE_TABLE = str.maketrans("", "", "₹,")


def clean_price_translate(price_str: str) -> float | None:
    """
    Convert a price string to float using str.translate (avoids two passes).

    >>> clean_price_translate("₹1,299")
    1299.0
    >>> clean_price_translate("₹899.99")
    899.99
    >>> clean_price_translate("N/A") is None
    True
    """
    try:
        return float(price_str.translate(_REMOVE_TABLE).strip())
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Approach 3 – regex extraction
# ---------------------------------------------------------------------------
import re
_PRICE_RE = re.compile(r"[\d,]+\.?\d*")


def clean_price_regex(price_str: str) -> float | None:
    """
    Extract numeric price from a price string using regex.

    >>> clean_price_regex("₹1,299")
    1299.0
    >>> clean_price_regex("₹45,000")
    45000.0
    >>> clean_price_regex("") is None
    True
    """
    m = _PRICE_RE.search(price_str)
    if not m:
        return None
    try:
        return float(m.group().replace(",", ""))
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    approaches = [
        ("strip+replace", clean_price_strip),
        ("translate", clean_price_translate),
        ("regex", clean_price_regex),
    ]
    sample = "₹1,299"
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(sample)
        elapsed = time.perf_counter() - t0
        print(f"{name:15s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
