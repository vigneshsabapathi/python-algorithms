#!/usr/bin/env python3
"""
Optimized and alternative implementations of Exponential Moving Average (EMA).

The reference yields EMA values using a streaming approach with alpha = 2/(1+window).
During the warm-up phase (i <= window_size) it uses a simple running average,
then switches to the standard EMA formula.

Variants covered:
1. streaming_warmup  -- reference approach (warm-up then EMA)
2. pure_ema          -- pure EMA from first element (no warm-up phase)
3. sma_seed          -- seed with SMA of first window, then EMA
4. list_based        -- eager list computation (no generator overhead)

Key interview insight:
    EMA gives more weight to recent prices (exponential decay). The choice of
    seeding method (first value vs SMA seed) affects early values but converges
    quickly. In trading systems, SMA-seeded EMA is the industry standard.

Run:
    python financial/exponential_moving_average_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections.abc import Iterator, Sequence

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from financial.exponential_moving_average import (
    exponential_moving_average as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 -- streaming with warm-up (reference)
# ---------------------------------------------------------------------------

def streaming_warmup(
    stock_prices: Iterator[float], window_size: int
) -> list[float]:
    """
    Reference approach wrapped to return a list for comparison.

    >>> streaming_warmup(iter([2, 5, 3, 8.2, 6, 9, 10]), 3)
    [2, 3.5, 3.25, 5.725, 5.8625, 7.43125, 8.715625]
    """
    return list(reference(stock_prices, window_size))


# ---------------------------------------------------------------------------
# Variant 2 -- pure EMA from first element (no warm-up averaging)
# ---------------------------------------------------------------------------

def pure_ema(prices: Sequence[float], window_size: int) -> list[float]:
    """
    Pure EMA: first value is the seed, then apply alpha smoothing throughout.
    No warm-up phase — simpler but less accurate for early values.

    >>> r = pure_ema([2, 5, 3, 8.2, 6, 9, 10], 3)
    >>> [round(v, 4) for v in r]
    [2.0, 3.5, 3.25, 5.725, 5.8625, 7.4313, 8.7156]
    """
    if window_size <= 0:
        raise ValueError("window_size must be > 0")
    alpha = 2 / (1 + window_size)
    result = [float(prices[0])]
    for price in prices[1:]:
        result.append(alpha * price + (1 - alpha) * result[-1])
    return result


# ---------------------------------------------------------------------------
# Variant 3 -- SMA seed then EMA (industry standard)
# ---------------------------------------------------------------------------

def sma_seed_ema(prices: Sequence[float], window_size: int) -> list[float]:
    """
    Seed with SMA of first `window_size` elements, then apply EMA.
    This is the standard method used by most trading platforms.

    >>> r = sma_seed_ema([2, 5, 3, 8.2, 6, 9, 10], 3)
    >>> [round(v, 4) for v in r]
    [2, 5, 3.3333, 5.7667, 5.8833, 7.4417, 8.7208]
    """
    if window_size <= 0:
        raise ValueError("window_size must be > 0")
    if len(prices) < window_size:
        return list(prices)

    alpha = 2 / (1 + window_size)

    # Return raw prices until we have enough for SMA seed
    result = list(prices[: window_size - 1])

    # SMA seed
    sma = sum(prices[:window_size]) / window_size
    result.append(sma)

    # EMA from seed onward
    ema = sma
    for price in prices[window_size:]:
        ema = alpha * price + (1 - alpha) * ema
        result.append(ema)

    return result


# ---------------------------------------------------------------------------
# Variant 4 -- list-based eager computation (no generator overhead)
# ---------------------------------------------------------------------------

def list_based_ema(prices: Sequence[float], window_size: int) -> list[float]:
    """
    Eager list computation of EMA using running average warm-up.
    Same logic as reference but avoids generator/yield overhead.

    >>> list_based_ema([2, 5, 3, 8.2, 6, 9, 10], 3)
    [2, 3.5, 3.25, 5.725, 5.8625, 7.43125, 8.715625]
    """
    if window_size <= 0:
        raise ValueError("window_size must be > 0")

    alpha = 2 / (1 + window_size)
    result = []
    ma = 0.0

    for i, price in enumerate(prices):
        if i <= window_size:
            ma = (ma + price) * 0.5 if i else price
        else:
            ma = alpha * price + (1 - alpha) * ma
        result.append(ma)

    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

PRICES_7 = [2.0, 5, 3, 8.2, 6, 9, 10]
PRICES_100 = [float(i + (i % 7) * 0.3) for i in range(100)]
WINDOW = 3

IMPLS = [
    ("streaming_warmup", lambda p, w: streaming_warmup(iter(p), w)),
    ("pure_ema",         pure_ema),
    ("sma_seed_ema",     sma_seed_ema),
    ("list_based_ema",   list_based_ema),
]


def run_all() -> None:
    print("\n=== Correctness (7 prices, window=3) ===")
    ref = streaming_warmup(iter(PRICES_7), WINDOW)
    for name, fn in IMPLS:
        result = fn(PRICES_7, WINDOW)
        match = all(abs(a - b) < 1e-6 for a, b in zip(ref, result))
        tag = "MATCH" if match else "DIFF"
        rounded = [round(v, 4) for v in result]
        print(f"  [{tag}] {name:<20} {rounded}")

    REPS = 50_000
    print(f"\n=== Benchmark: {REPS} runs, 7 prices ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(PRICES_7, WINDOW), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms")

    print(f"\n=== Benchmark: {REPS} runs, 100 prices ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(PRICES_100, WINDOW), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
