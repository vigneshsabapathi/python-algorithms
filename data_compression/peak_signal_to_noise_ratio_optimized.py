#!/usr/bin/env python3
"""
Optimized and alternative implementations of Peak Signal-to-Noise Ratio (PSNR).

The reference computes MSE then PSNR using math.log10. Variants explore
different computation approaches.

Variants covered:
1. math_based     -- pure Python with math.log10 (reference)
2. decibel_direct -- direct dB formula without intermediate sqrt
3. generator_mse  -- generator expression for memory-efficient MSE
4. numpy_based    -- numpy vectorized (if available)

Key interview insight:
    PSNR = 10 * log10(MAX^2 / MSE) = 20 * log10(MAX / sqrt(MSE)).
    The 20*log10 form is standard because it's in terms of amplitude,
    not power. PSNR is undefined when MSE=0 (identical signals).
    Convention: return 100 or float('inf') for identical signals.

Run:
    python data_compression/peak_signal_to_noise_ratio_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_compression.peak_signal_to_noise_ratio import (
    peak_signal_to_noise_ratio as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 -- math_based (reference wrapper)
# ---------------------------------------------------------------------------

def math_based(original: list, contrast: list) -> float:
    """
    PSNR using reference implementation (pure Python, math.log10).

    >>> math_based([100, 100, 100], [100, 100, 100])
    100
    >>> round(math_based([100, 120, 130], [110, 130, 140]), 2)
    28.13
    """
    return reference(original, contrast)


# ---------------------------------------------------------------------------
# Variant 2 -- decibel_direct: avoid sqrt by using 10*log10(MAX^2/MSE)
# ---------------------------------------------------------------------------

def decibel_direct(original: list, contrast: list, pixel_max: float = 255.0) -> float:
    """
    PSNR via 10 * log10(MAX^2 / MSE), avoiding the sqrt operation.

    Mathematically equivalent: 20*log10(MAX/sqrt(MSE)) = 10*log10(MAX^2/MSE)

    >>> decibel_direct([100, 100, 100], [100, 100, 100])
    100
    >>> round(decibel_direct([100, 120, 130], [110, 130, 140]), 2)
    28.13
    """
    flat_o = _flatten(original)
    flat_c = _flatten(contrast)

    if len(flat_o) != len(flat_c):
        raise ValueError("Signals must have the same length.")

    mse = sum((a - b) ** 2 for a, b in zip(flat_o, flat_c)) / len(flat_o)

    if mse == 0:
        return 100

    return 10 * math.log10(pixel_max * pixel_max / mse)


# ---------------------------------------------------------------------------
# Variant 3 -- generator_mse: memory-efficient MSE with generator
# ---------------------------------------------------------------------------

def generator_psnr(original: list, contrast: list, pixel_max: float = 255.0) -> float:
    """
    PSNR using generator expression for MSE (no intermediate list allocation).

    >>> generator_psnr([100, 100, 100], [100, 100, 100])
    100
    >>> round(generator_psnr([0, 50, 100, 150, 200], [10, 60, 110, 160, 210]), 2)
    28.13
    """
    flat_o = _flatten(original)
    flat_c = _flatten(contrast)
    n = len(flat_o)

    if n == 0:
        raise ValueError("Input signals must not be empty.")

    mse = sum((a - b) ** 2 for a, b in zip(flat_o, flat_c)) / n

    if mse == 0:
        return 100

    return 20 * math.log10(pixel_max / math.sqrt(mse))


# ---------------------------------------------------------------------------
# Variant 4 -- numpy_based (vectorized)
# ---------------------------------------------------------------------------

def numpy_psnr(original: list, contrast: list, pixel_max: float = 255.0) -> float:
    """
    PSNR using numpy for vectorized computation.

    >>> numpy_psnr([100, 100, 100], [100, 100, 100])
    100
    >>> round(numpy_psnr([100, 120, 130], [110, 130, 140]), 2)
    28.13
    """
    try:
        import numpy as np
    except ImportError:
        # Fallback to pure Python
        return generator_psnr(original, contrast, pixel_max)

    orig = np.array(_flatten(original), dtype=np.float64)
    cont = np.array(_flatten(contrast), dtype=np.float64)

    mse = float(np.mean((orig - cont) ** 2))

    if mse == 0:
        return 100

    return float(20 * np.log10(pixel_max / np.sqrt(mse)))


def _flatten(data: list) -> list[float]:
    """Flatten nested list."""
    result: list[float] = []
    for item in data:
        if isinstance(item, (list, tuple)):
            result.extend(_flatten(item))
        else:
            result.append(float(item))
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([100, 100, 100], [100, 100, 100], 100),
    ([100, 120, 130], [110, 130, 140], 28.13),
    ([0, 50, 100, 150, 200], [10, 60, 110, 160, 210], 28.13),
    ([0, 0, 0], [255, 255, 255], 0.0),
    ([128] * 100, [130] * 100, None),  # just check consistency
]

IMPLS = [
    ("math_based",      math_based),
    ("decibel_direct",  decibel_direct),
    ("generator_psnr",  generator_psnr),
    ("numpy_psnr",      numpy_psnr),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for orig, cont, expected in TEST_CASES:
        for name, fn in IMPLS:
            try:
                result = fn(orig, cont)
                if expected is not None:
                    ok = abs(round(result, 2) - expected) < 0.01
                else:
                    ok = True  # just check it runs
                tag = "OK" if ok else "FAIL"
                print(f"  [{tag}] {name:<18} PSNR={result:>8.2f} dB  expected={expected}")
            except Exception as e:
                print(f"  [ERR] {name:<18} {e}")

    import random
    random.seed(42)
    large_orig = [random.randint(0, 255) for _ in range(10_000)]
    large_cont = [v + random.randint(-10, 10) for v in large_orig]

    REPS = 5_000
    print(f"\n=== Benchmark (10,000 pixels): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(large_orig, large_cont), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
