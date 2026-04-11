#!/usr/bin/env python3
"""
Optimized and alternative implementations of Simple Moving Average (SMA).

The reference iterates through data, slicing a window each time and computing
the mean. This is O(n*w) where n = data length and w = window size.

Variants covered:
1. slice_window     -- reference (slice + sum each step)
2. rolling_sum      -- O(n) sliding window with running sum
3. cumsum_trick     -- prefix sum array for O(1) per-window lookup
4. deque_window     -- collections.deque for explicit sliding window

Key interview insight:
    The naive slice approach is O(n*w). The rolling sum / prefix sum approaches
    reduce to O(n). For streaming data (unknown length), the deque approach is
    ideal since it doesn't require the full dataset upfront.

Run:
    python financial/simple_moving_average_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import deque
from collections.abc import Sequence

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from financial.simple_moving_average import simple_moving_average as reference


# ---------------------------------------------------------------------------
# Variant 1 -- slice window (reference)
# ---------------------------------------------------------------------------

def slice_window(data: Sequence[float], window_size: int) -> list[float | None]:
    """
    Reference: slice a window at each step and compute the mean.

    >>> r = slice_window([10, 12, 15, 13, 14, 16, 18, 17, 19, 21], 3)
    >>> [round(v, 2) if v is not None else None for v in r]
    [None, None, 12.33, 13.33, 14.0, 14.33, 16.0, 17.0, 18.0, 19.0]
    """
    return reference(data, window_size)


# ---------------------------------------------------------------------------
# Variant 2 -- rolling sum O(n)
# ---------------------------------------------------------------------------

def rolling_sum(data: Sequence[float], window_size: int) -> list[float | None]:
    """
    Maintain a running sum: add new element, subtract oldest. O(n) total.

    >>> r = rolling_sum([10, 12, 15, 13, 14, 16, 18, 17, 19, 21], 3)
    >>> [round(v, 2) if v is not None else None for v in r]
    [None, None, 12.33, 13.33, 14.0, 14.33, 16.0, 17.0, 18.0, 19.0]
    >>> rolling_sum([10, 12, 15], 5)
    [None, None, None]
    """
    if window_size < 1:
        raise ValueError("Window size must be a positive integer")

    result: list[float | None] = [None] * min(window_size - 1, len(data))
    if len(data) < window_size:
        return result

    window_sum = sum(data[:window_size])
    result.append(window_sum / window_size)

    for i in range(window_size, len(data)):
        window_sum += data[i] - data[i - window_size]
        result.append(window_sum / window_size)

    return result


# ---------------------------------------------------------------------------
# Variant 3 -- prefix (cumulative) sum trick
# ---------------------------------------------------------------------------

def cumsum_trick(data: Sequence[float], window_size: int) -> list[float | None]:
    """
    Build prefix sum array, then SMA[i] = (prefix[i+1] - prefix[i-w+1]) / w.
    O(n) build + O(1) per query.

    >>> r = cumsum_trick([10, 12, 15, 13, 14, 16, 18, 17, 19, 21], 3)
    >>> [round(v, 2) if v is not None else None for v in r]
    [None, None, 12.33, 13.33, 14.0, 14.33, 16.0, 17.0, 18.0, 19.0]
    """
    if window_size < 1:
        raise ValueError("Window size must be a positive integer")

    n = len(data)
    if n < window_size:
        return [None] * n

    # Build prefix sums: prefix[i] = sum(data[0:i])
    prefix = [0.0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + data[i]

    result: list[float | None] = [None] * (window_size - 1)
    for i in range(window_size - 1, n):
        sma = (prefix[i + 1] - prefix[i - window_size + 1]) / window_size
        result.append(sma)

    return result


# ---------------------------------------------------------------------------
# Variant 4 -- deque-based sliding window (streaming friendly)
# ---------------------------------------------------------------------------

def deque_window(data: Sequence[float], window_size: int) -> list[float | None]:
    """
    Uses collections.deque with maxlen for explicit sliding window.
    Ideal for streaming data where you process one element at a time.

    >>> r = deque_window([10, 12, 15, 13, 14, 16, 18, 17, 19, 21], 3)
    >>> [round(v, 2) if v is not None else None for v in r]
    [None, None, 12.33, 13.33, 14.0, 14.33, 16.0, 17.0, 18.0, 19.0]
    """
    if window_size < 1:
        raise ValueError("Window size must be a positive integer")

    window: deque[float] = deque(maxlen=window_size)
    result: list[float | None] = []
    window_sum = 0.0

    for val in data:
        if len(window) == window_size:
            window_sum -= window[0]
        window.append(val)
        window_sum += val

        if len(window) < window_size:
            result.append(None)
        else:
            result.append(window_sum / window_size)

    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

DATA_10 = [10, 12, 15, 13, 14, 16, 18, 17, 19, 21]
DATA_1000 = [float(i + (i % 13) * 0.5) for i in range(1000)]
WINDOW = 3

IMPLS = [
    ("slice_window",  slice_window),
    ("rolling_sum",   rolling_sum),
    ("cumsum_trick",  cumsum_trick),
    ("deque_window",  deque_window),
]


def run_all() -> None:
    print("\n=== Correctness (10 elements, window=3) ===")
    ref = reference(DATA_10, WINDOW)
    ref_rounded = [round(v, 6) if v is not None else None for v in ref]
    for name, fn in IMPLS:
        result = fn(DATA_10, WINDOW)
        rounded = [round(v, 6) if v is not None else None for v in result]
        match = rounded == ref_rounded
        tag = "MATCH" if match else "DIFF"
        display = [round(v, 2) if v is not None else None for v in result]
        print(f"  [{tag}] {name:<14} {display}")

    REPS = 20_000

    print(f"\n=== Benchmark: {REPS} runs, 10 elements, window=3 ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(DATA_10, WINDOW), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms")

    print(f"\n=== Benchmark: {REPS} runs, 1000 elements, window=20 ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(DATA_1000, 20), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
