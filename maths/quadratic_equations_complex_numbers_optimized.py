"""
Numerically stable quadratic solver + benchmark.

1. naive_formula     - direct quadratic formula (suffers catastrophic cancellation)
2. stable_formula    - use Citardauq/"alternate" form to avoid cancellation
3. numpy_roots       - numpy.roots polynomial solver
"""
from __future__ import annotations

import cmath
import time


def naive_formula(a, b, c):
    d = cmath.sqrt(b * b - 4 * a * c)
    return (-b + d) / (2 * a), (-b - d) / (2 * a)


def stable_formula(a, b, c):
    """
    Use x1 = (-b - sign(b) * sqrt(disc)) / (2a), x2 = c / (a*x1).
    Avoids subtracting nearly equal quantities.
    """
    d = cmath.sqrt(b * b - 4 * a * c)
    # pick sign to match sign of Re(b)
    sign = 1 if (b.real if isinstance(b, complex) else b) >= 0 else -1
    x1 = (-b - sign * d) / (2 * a)
    if x1 == 0:
        x2 = (-b + sign * d) / (2 * a)
    else:
        x2 = c / (a * x1)
    return x1, x2


def numpy_roots(a, b, c):
    try:
        import numpy as np
    except ImportError:
        return naive_formula(a, b, c)
    r = np.roots([a, b, c])
    return complex(r[0]), complex(r[1])


def benchmark():
    cases = [(1, -3, 2), (1, 1e8, 1), (1, 2, 5)]
    print(f"{'fn':<16}{'coeffs':>24}{'roots':>50}{'ms':>10}")
    for fn in (naive_formula, stable_formula, numpy_roots):
        for coef in cases:
            t = time.perf_counter()
            for _ in range(10000):
                r = fn(*coef)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<16}{str(coef):>24}{str(r):>50}{dt:>10.3f}")


if __name__ == "__main__":
    benchmark()
