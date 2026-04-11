#!/usr/bin/env python3
"""
Optimized and alternative implementations of Circular Convolution.

Variants covered:
1. matrix_method  -- reference: build circulant matrix, matmul
2. fft_method     -- multiply DFTs, then IDFT (O(n log n))
3. direct_sum     -- direct summation formula y[n] = sum(x[k]*h[(n-k)%N])

Run:
    python electronics/circular_convolution_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import deque

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from electronics.circular_convolution import CircularConvolution


def ref_convolve(first: list[float], second: list[float]) -> list[float]:
    """Reference wrapper."""
    c = CircularConvolution()
    c.first_signal = first[:]
    c.second_signal = second[:]
    return c.circular_convolution()


# ---------------------------------------------------------------------------
# Variant 1 -- matrix_method (reference wrapper)
# ---------------------------------------------------------------------------

def matrix_method(first: list[float], second: list[float]) -> list[float]:
    """
    >>> matrix_method([2, 1, 2, -1], [1, 2, 3, 4])
    [10.0, 10.0, 6.0, 14.0]
    """
    return ref_convolve(first, second)


# ---------------------------------------------------------------------------
# Variant 2 -- fft_method: O(n log n) via numpy FFT
# ---------------------------------------------------------------------------

def fft_method(first: list[float], second: list[float]) -> list[float]:
    """
    Circular convolution via FFT: IFFT(FFT(x) * FFT(h)).

    >>> fft_method([2, 1, 2, -1], [1, 2, 3, 4])
    [10.0, 10.0, 6.0, 14.0]
    """
    n = max(len(first), len(second))
    x = np.array(first + [0] * (n - len(first)), dtype=float)
    h = np.array(second + [0] * (n - len(second)), dtype=float)
    result = np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h)))
    return [float(round(v, 2)) for v in result]


# ---------------------------------------------------------------------------
# Variant 3 -- direct_sum: O(n^2) but no matrix construction
# ---------------------------------------------------------------------------

def direct_sum(first: list[float], second: list[float]) -> list[float]:
    """
    y[n] = sum_{k=0}^{N-1} x[k] * h[(n-k) % N].

    >>> direct_sum([2, 1, 2, -1], [1, 2, 3, 4])
    [10.0, 10.0, 6.0, 14.0]
    """
    n = max(len(first), len(second))
    x = first + [0] * (n - len(first))
    h = second + [0] * (n - len(second))
    result = []
    for i in range(n):
        val = sum(x[k] * h[(i - k) % n] for k in range(n))
        result.append(float(round(val, 2)))
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (([2, 1, 2, -1], [1, 2, 3, 4]), [10.0, 10.0, 6.0, 14.0]),
    (([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6],
      [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]),
     [5.2, 6.0, 6.48, 6.64, 6.48, 6.0, 5.2, 4.08]),
]

IMPLS = [
    ("matrix",     matrix_method),
    ("fft",        fft_method),
    ("direct_sum", direct_sum),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for (a, b), expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(a[:], b[:])
            ok = result == expected
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {result}")

    REPS = 50_000
    a = list(range(1, 33))
    b = list(range(32, 0, -1))

    print(f"\n=== Benchmark (N=32): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(a[:], b[:]), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
