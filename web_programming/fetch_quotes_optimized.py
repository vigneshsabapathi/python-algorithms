"""
Fetch Quotes – three quote-parsing approaches + benchmark.

Approach 1: dict key access (standard)
Approach 2: .get() with fallback (safe)
Approach 3: destructuring via tuple unpacking helper
"""

import time


SAMPLE_RESPONSE = [
    {"q": "Be yourself; everyone else is already taken.", "a": "Oscar Wilde", "h": "<blockquote>...</blockquote>"},
    {"q": "Live as if you were to die tomorrow.", "a": "Mahatma Gandhi", "h": "<blockquote>...</blockquote>"},
]


# ---------------------------------------------------------------------------
# Approach 1 – dict key access
# ---------------------------------------------------------------------------
def parse_quote_key(quote_obj: dict) -> tuple[str, str]:
    """
    Extract (quote, author) using direct key access.

    >>> parse_quote_key({"q": "Hello", "a": "World", "h": ""})
    ('Hello', 'World')
    """
    return quote_obj["q"], quote_obj["a"]


# ---------------------------------------------------------------------------
# Approach 2 – .get() with fallback
# ---------------------------------------------------------------------------
def parse_quote_get(quote_obj: dict, default: str = "Unknown") -> tuple[str, str]:
    """
    Extract (quote, author) using .get() with a fallback value.

    >>> parse_quote_get({"q": "Hello", "a": "World", "h": ""})
    ('Hello', 'World')
    >>> parse_quote_get({})
    ('Unknown', 'Unknown')
    >>> parse_quote_get({"q": "Only quote"})
    ('Only quote', 'Unknown')
    """
    return quote_obj.get("q", default), quote_obj.get("a", default)


# ---------------------------------------------------------------------------
# Approach 3 – itemgetter
# ---------------------------------------------------------------------------
from operator import itemgetter

_get_qa = itemgetter("q", "a")


def parse_quote_itemgetter(quote_obj: dict) -> tuple[str, str]:
    """
    Extract (quote, author) using operator.itemgetter (fast for repeated calls).

    >>> parse_quote_itemgetter({"q": "Hello", "a": "World", "h": ""})
    ('Hello', 'World')
    """
    return _get_qa(quote_obj)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    approaches = [
        ("key access", parse_quote_key),
        ("get fallback", parse_quote_get),
        ("itemgetter", parse_quote_itemgetter),
    ]
    obj = SAMPLE_RESPONSE[0]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(obj)
        elapsed = time.perf_counter() - t0
        print(f"{name:15s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
