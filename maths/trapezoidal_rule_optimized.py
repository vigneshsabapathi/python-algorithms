"""
Numerical integration variants + benchmark.

1. trapezoidal     - O(n), 2nd-order accurate
2. simpson         - O(n), 4th-order accurate (n even)
3. romberg         - Richardson-extrapolated trapezoid
4. numpy_trapz     - vectorized
"""
from __future__ import annotations

import math
import time
from typing import Callable


def trapezoidal(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


def simpson(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    if n % 2:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n, 2):
        s += 4 * f(a + i * h)
    for i in range(2, n, 2):
        s += 2 * f(a + i * h)
    return s * h / 3


def romberg(f, a, b, depth=5):
    R = [[0.0] * (depth + 1) for _ in range(depth + 1)]
    R[0][0] = 0.5 * (b - a) * (f(a) + f(b))
    for k in range(1, depth + 1):
        h = (b - a) / (2**k)
        R[k][0] = 0.5 * R[k - 1][0] + h * sum(f(a + (2 * i - 1) * h) for i in range(1, 2 ** (k - 1) + 1))
        for j in range(1, k + 1):
            R[k][j] = R[k][j - 1] + (R[k][j - 1] - R[k - 1][j - 1]) / (4**j - 1)
    return R[depth][depth]


def numpy_trapz(f, a, b, n):
    try:
        import numpy as np
    except ImportError:
        return trapezoidal(f, a, b, n)
    xs = np.linspace(a, b, n + 1)
    ys = np.array([f(x) for x in xs])
    return float(np.trapz(ys, xs))


def benchmark() -> None:
    g = math.sin
    true = 2.0
    print(f"{'fn':<14}{'n':>6}{'value':>14}{'err':>14}{'ms':>10}")
    for n in (10, 100, 1000):
        for fn in (trapezoidal, simpson, numpy_trapz):
            t = time.perf_counter()
            v = fn(g, 0, math.pi, n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<14}{n:>6}{v:>14.8f}{abs(v - true):>14.2e}{dt:>10.3f}")
    print(f"romberg depth=6 -> {romberg(g, 0, math.pi, 6):.10f}")


if __name__ == "__main__":
    benchmark()
