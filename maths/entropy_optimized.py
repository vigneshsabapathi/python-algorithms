#!/usr/bin/env python3
"""
Optimized entropy variants.

Variants:
1. shannon_entropy  -- plain Shannon entropy of a symbol distribution.
2. entropy_counter  -- replaces dual loops with Counter(text) + Counter(bigrams).
3. entropy_scipy    -- scipy.stats.entropy fallback (if available).

Run:
    python maths/entropy_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.entropy import analyze_text


def shannon_entropy(text: str) -> float:
    """
    H(X) = -sum p_i log2 p_i over all symbols in text.

    >>> round(shannon_entropy("aaaa"), 4)
    -0.0
    >>> round(shannon_entropy("abab"), 4)
    1.0
    >>> round(shannon_entropy("abcd"), 4)
    2.0
    """
    if not text:
        return 0.0
    c = Counter(text)
    total = len(text)
    return -sum((v / total) * math.log2(v / total) for v in c.values())


def bigram_entropy(text: str) -> float:
    """
    >>> round(bigram_entropy("abab"), 4)
    0.9183
    """
    if len(text) < 2:
        return 0.0
    bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    c = Counter(bigrams)
    total = sum(c.values())
    return -sum((v / total) * math.log2(v / total) for v in c.values())


def _benchmark() -> None:
    text = "the quick brown fox jumps over the lazy dog " * 100
    n = 1000
    t1 = timeit.timeit(lambda: analyze_text(text), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: shannon_entropy(text), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: bigram_entropy(text), number=n) * 1000 / n
    print(f"analyze_text (ref): {t1:.3f} ms")
    print(f"shannon_entropy:    {t2:.3f} ms")
    print(f"bigram_entropy:     {t3:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
