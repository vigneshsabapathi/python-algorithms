"""
Giphy – three query-formatting approaches + benchmark.

Approach 1: str.join with split (original)
Approach 2: urllib.parse.quote_plus
Approach 3: replace spaces
"""

import time
from urllib.parse import quote_plus


# ---------------------------------------------------------------------------
# Approach 1 – str.join + split (original)
# ---------------------------------------------------------------------------
def format_query_join(query: str) -> str:
    """
    Format a Giphy query by joining words with '+'.

    >>> format_query_join("space ship")
    'space+ship'
    >>> format_query_join("cat playing piano")
    'cat+playing+piano'
    """
    return "+".join(query.split())


# ---------------------------------------------------------------------------
# Approach 2 – urllib.parse.quote_plus
# ---------------------------------------------------------------------------
def format_query_quote_plus(query: str) -> str:
    """
    Format a Giphy query using urllib.parse.quote_plus (handles special chars).

    >>> format_query_quote_plus("space ship")
    'space+ship'
    >>> format_query_quote_plus("cat & dog")
    'cat+%26+dog'
    """
    return quote_plus(query)


# ---------------------------------------------------------------------------
# Approach 3 – str.replace
# ---------------------------------------------------------------------------
def format_query_replace(query: str) -> str:
    """
    Format a Giphy query by replacing spaces with '+'.

    >>> format_query_replace("space ship")
    'space+ship'
    >>> format_query_replace("happy new year")
    'happy+new+year'
    """
    return query.replace(" ", "+")


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    query = "funny space cats"
    approaches = [
        ("join+split", format_query_join),
        ("quote_plus", format_query_quote_plus),
        ("replace", format_query_replace),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(query)
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
