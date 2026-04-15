"""
Pi digit generation: multiple algorithms + benchmark.

1. spigot       - Gibbons unbounded spigot
2. leibniz      - arctan(1) = 1 - 1/3 + 1/5 - ...  (very slow convergence)
3. machin       - Machin's formula via Decimal getcontext precision
4. chudnovsky   - Chudnovsky series (fast, ~14 digits per term)
"""
from __future__ import annotations

import time
from decimal import Decimal, getcontext


def spigot(n_digits: int) -> str:
    q, r, t, i = 1, 180, 60, 2
    out = []
    while len(out) < n_digits:
        u = 3 * (3 * i + 1) * (3 * i + 2)
        y = (q * (27 * i - 12) + 5 * r) // (5 * t)
        out.append(str(y))
        q, r, t, i = 10 * q * i * (2 * i - 1), 10 * u * (q * (5 * i - 2) + r - y * t), t * u, i + 1
    return out[0] + "." + "".join(out[1:])


def leibniz(n_terms: int) -> float:
    s = 0.0
    for k in range(n_terms):
        s += ((-1) ** k) / (2 * k + 1)
    return 4 * s


def machin(n_digits: int) -> str:
    getcontext().prec = n_digits + 5

    def arctan(x: Decimal) -> Decimal:
        x2 = x * x
        term = x
        s = Decimal(0)
        k = 0
        while term != 0:
            s += term / (2 * k + 1) * ((-1) ** k)
            term *= x2
            k += 1
        return s

    pi = 16 * arctan(Decimal(1) / 5) - 4 * arctan(Decimal(1) / 239)
    return str(pi)[: n_digits + 1]


def chudnovsky(n_digits: int) -> str:
    getcontext().prec = n_digits + 10
    C = 426880 * Decimal(10005).sqrt()
    M, L, X, K, S = Decimal(1), Decimal(13591409), Decimal(1), Decimal(6), Decimal(13591409)
    for i in range(1, n_digits // 14 + 2):
        M = (M * (K**3 - 16 * K)) / Decimal(i) ** 3
        L += 545140134
        X *= -262537412640768000
        S += Decimal(M * L) / X
        K += 12
    pi = C / S
    return str(pi)[: n_digits + 1]


def benchmark() -> None:
    print(f"{'fn':<14}{'digits':>8}{'ms':>14}")
    for fn in (spigot, machin, chudnovsky):
        for d in (20, 100, 500):
            t = time.perf_counter()
            fn(d)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<14}{d:>8}{dt:>14.3f}")


if __name__ == "__main__":
    benchmark()
