#!/usr/bin/env python3
"""
Optimized binomial_distribution variants.

Reference: factorial formula P = C(n,k) * p^k * (1-p)^(n-k).

Variants:
1. binom_mathcomb   -- math.comb instead of 3 factorials; O(k) instead of O(n).
2. binom_scipy      -- scipy.stats.binom.pmf (if scipy available).
3. binom_log        -- log-space computation for large n (avoids overflow).

Run:
    python maths/binomial_distribution_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.binomial_distribution import binomial_distribution as bd_ref


def binom_mathcomb(successes: int, trials: int, prob: float) -> float:
    """
    >>> round(binom_mathcomb(3, 5, 0.7), 5)
    0.3087
    >>> binom_mathcomb(2, 4, 0.5)
    0.375
    """
    if successes > trials or trials < 0 or successes < 0:
        raise ValueError("invalid")
    if not 0 < prob < 1:
        raise ValueError("prob out of range")
    return math.comb(trials, successes) * prob ** successes * (1 - prob) ** (trials - successes)


def binom_log(successes: int, trials: int, prob: float) -> float:
    """
    Log-space for very large n (n=10000+) where factorials overflow floats.

    >>> round(binom_log(50, 100, 0.5), 6)
    0.079589
    """
    if successes > trials or trials < 0 or successes < 0 or not 0 < prob < 1:
        raise ValueError("invalid")
    lg = math.lgamma(trials + 1) - math.lgamma(successes + 1) - math.lgamma(trials - successes + 1)
    lp = successes * math.log(prob) + (trials - successes) * math.log(1 - prob)
    return math.exp(lg + lp)


def _benchmark() -> None:
    n = 50000
    t1 = timeit.timeit(lambda: bd_ref(50, 100, 0.5), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: binom_mathcomb(50, 100, 0.5), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: binom_log(50, 100, 0.5), number=n) * 1000 / n
    print(f"reference factorial: {t1:.5f} ms")
    print(f"math.comb:           {t2:.5f} ms  [{t1/t2:.2f}x]")
    print(f"log-space:           {t3:.5f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
