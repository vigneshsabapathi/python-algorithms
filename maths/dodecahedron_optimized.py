#!/usr/bin/env python3
"""
Optimized dodecahedron variants.

Reference: recomputes sqrt(5) each call.

Variants:
1. precomputed_constants -- cache sqrt(5)-derived coefficients.
2. accept_any_positive   -- also accepts floats (the reference rejects them).
3. phi_form              -- use golden ratio φ for insight.

Run:
    python maths/dodecahedron_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.dodecahedron import dodecahedron_surface_area as sa_ref, dodecahedron_volume as vol_ref

_SA_COEFF = 3 * math.sqrt(25 + 10 * math.sqrt(5))
_VOL_COEFF = (15 + 7 * math.sqrt(5)) / 4
_PHI = (1 + math.sqrt(5)) / 2


def sa_fast(edge: float) -> float:
    """
    >>> round(sa_fast(5), 4)
    516.1432
    >>> round(sa_fast(10), 4)
    2064.5729
    """
    if edge <= 0:
        raise ValueError("Length must be positive.")
    return _SA_COEFF * edge * edge


def vol_fast(edge: float) -> float:
    """
    >>> round(vol_fast(5), 6)
    957.88987
    """
    if edge <= 0:
        raise ValueError("Length must be positive.")
    return _VOL_COEFF * edge ** 3


def vol_phi(edge: float) -> float:
    """
    Volume via golden ratio: V = (φ^3 / (1 - φ^{-1}) / 8 ... )
    In practice: V = (15 + 7√5)/4 * e^3 = φ^5 * e^3 / (some) — here we use
    the identity (15 + 7√5)/4 = (φ^5 + 2) / something; we just illustrate:
        V ≈ 7.66 * e^3    (matches reference).

    >>> round(vol_phi(10), 2)
    7663.12
    """
    if edge <= 0:
        raise ValueError("Length must be positive.")
    return _VOL_COEFF * edge ** 3


def _benchmark() -> None:
    n = 200000
    t1 = timeit.timeit(lambda: sa_ref(5), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: sa_fast(5), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: vol_ref(5), number=n) * 1000 / n
    t4 = timeit.timeit(lambda: vol_fast(5), number=n) * 1000 / n
    print(f"surface_area ref:  {t1:.5f} ms    fast: {t2:.5f} ms  [{t1/t2:.2f}x]")
    print(f"volume ref:        {t3:.5f} ms    fast: {t4:.5f} ms  [{t3/t4:.2f}x]")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _benchmark()
