"""Maclaurin series — variants + benchmark."""

import math
import time


def sin_naive(x, terms=20):
    r = 0.0
    for n in range(terms):
        r += ((-1) ** n) * (x ** (2 * n + 1)) / math.factorial(2 * n + 1)
    return r


def sin_horner_like(x, terms=20):
    """Compute term from previous: t_{n+1} = t_n * (-x²) / ((2n+2)(2n+3))."""
    term = x
    total = term
    for n in range(1, terms):
        term *= -(x * x) / ((2 * n) * (2 * n + 1))
        total += term
    return total


def sin_math(x):
    return math.sin(x)


def benchmark():
    x = 1.2
    for name, fn in [
        ("naive_factorial", lambda: sin_naive(x, 20)),
        ("incremental_term", lambda: sin_horner_like(x, 20)),
        ("math.sin", lambda: sin_math(x)),
    ]:
        start = time.perf_counter()
        for _ in range(10_000):
            fn()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} sin(1.2)={fn():.8f}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
