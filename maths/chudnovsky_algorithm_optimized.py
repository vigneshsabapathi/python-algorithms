#!/usr/bin/env python3
"""
Optimized Chudnovsky (pi) variants.

Reference: per-iteration factorials via math.factorial.

Variants:
1. pi_incremental_m -- update multinomial_term incrementally (skip factorials).
2. pi_mpmath        -- delegate to mpmath (if available; production-grade).
3. pi_math_pi       -- just math.pi (reference check for precision<=15).

Run:
    python maths/chudnovsky_algorithm_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit
from decimal import Decimal, getcontext

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.chudnovsky_algorithm import pi as pi_ref


def pi_incremental(precision: int) -> str:
    """
    Chudnovsky with incrementally-updated multinomial coefficient:
        M_{k+1} = M_k * (6k+1)(6k+2)(6k+3)(6k+4)(6k+5)(6k+6) / ((3k+1)(3k+2)(3k+3) * (k+1)^3)

    >>> pi_incremental(10)
    '3.14159265'
    >>> pi_incremental(50).startswith('3.14159265358979323846264338327950288419716939937')
    True
    """
    if not isinstance(precision, int):
        raise TypeError("Undefined for non-integers")
    if precision < 1:
        raise ValueError("Undefined for non-natural numbers")
    getcontext().prec = precision
    num_iter = math.ceil(precision / 14)
    constant = 426880 * Decimal(10005).sqrt()
    exp_term = 1
    linear = 13591409
    partial = Decimal(linear)
    m_term = 1
    for k in range(1, num_iter):
        # M_k = (6k)!/((3k)!*(k!)^3) updated from M_{k-1}
        m_term = m_term * (
            (6 * k - 5) * (6 * k - 4) * (6 * k - 3) * (6 * k - 2) * (6 * k - 1) * (6 * k)
        ) // ((3 * k - 2) * (3 * k - 1) * (3 * k) * k * k * k)
        linear += 545140134
        exp_term *= -262537412640768000
        partial += Decimal(m_term * linear) / exp_term
    return str(constant / partial)[:-1]


def _benchmark() -> None:
    n = 5
    for p in (50, 200, 500):
        t1 = timeit.timeit(lambda: pi_ref(p), number=n) * 1000 / n
        t2 = timeit.timeit(lambda: pi_incremental(p), number=n) * 1000 / n
        print(f"precision={p:>4}:  reference={t1:.2f} ms  incremental={t2:.2f} ms  [{t1/t2:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
