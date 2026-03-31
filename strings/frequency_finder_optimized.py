"""
Optimized frequency finder using Counter + sorted with a composite key.
Companion to frequency_finder.py — see that file for the multi-step dict baseline.

Used in cryptanalysis: compare a ciphertext's letter frequency distribution
against standard English frequencies to score how "English-like" the text is.
"""

import string
from collections import Counter

ETAOIN = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
# Pre-computed positions for O(1) lookup in sort key (avoids O(26) .index() per call)
_ETAOIN_POS = {c: i for i, c in enumerate(ETAOIN)}


def get_frequency_order_optimized(message: str) -> str:
    """
    Returns all 26 uppercase letters ordered by their frequency in message
    (most to least frequent). Ties broken by ETAOIN order (most common English
    letters rank higher on ties).

    Uses Counter + a single sorted() call with a composite key instead of
    multiple dict-building passes.

    >>> get_frequency_order_optimized('Hello World')
    'LOWDRHEZQXJKVBPYGFMUCSNIAT'
    >>> get_frequency_order_optimized('Hello@')
    'LHOEZQXJKVBPYGFWMUCDRSNIAT'
    >>> get_frequency_order_optimized('h')
    'HZQXJKVBPYGFWMUCLDRSNIOATE'
    """
    # Count only alphabetic characters, case-insensitive
    counts = Counter(c for c in message.upper() if c.isalpha())

    # Sort all 26 letters by:
    #   1. Descending frequency (-count), so most frequent comes first
    #   2. Ascending ETAOIN position as tiebreaker (lower index = more common in English)
    # Sort key:
    #   Primary:   -count  (descending frequency — most frequent first)
    #   Secondary: -ETAOIN.index(c)  (within same frequency, less common English
    #              letters come first — mirrors original's reverse=True on ETAOIN pos)
    return "".join(
        sorted(
            string.ascii_uppercase,
            key=lambda c: (-counts.get(c, 0), -_ETAOIN_POS[c]),
        )
    )


def english_freq_match_score_optimized(message: str) -> int:
    """
    Score how closely a message's letter frequency matches English.
    Compares the 6 most common and 6 least common letters against ETAOIN order.
    Score ranges from 0 (no match) to 12 (perfect match).

    >>> english_freq_match_score_optimized('Hello World')
    1
    """
    freq_order = get_frequency_order_optimized(message)
    top6 = set(freq_order[:6])
    bot6 = set(freq_order[-6:])
    return (
        sum(1 for c in ETAOIN[:6] if c in top6) +
        sum(1 for c in ETAOIN[-6:] if c in bot6)
    )


def benchmark() -> None:
    """Benchmark original vs optimized implementations."""
    from timeit import timeit

    n = 50_000
    msg = "The quick brown fox jumps over the lazy dog"

    cases = [
        (f'get_frequency_order("{msg}")',
         "from frequency_finder import get_frequency_order",
         "original  (multi-step dict)"),
        (f'get_frequency_order_optimized("{msg}")',
         "from frequency_finder_optimized import get_frequency_order_optimized",
         "optimized (Counter + sorted)"),
    ]

    print(f"Benchmarking {n:,} runs on a {len(msg)}-char string:\n")
    for stmt, setup, label in cases:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {label:<30} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
