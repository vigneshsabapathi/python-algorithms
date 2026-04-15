"""Gamma — variants + benchmark."""

import math
import time


def gamma_builtin(x):
    return math.gamma(x)


def gamma_lanczos(x):
    """Lanczos approximation — fast and accurate."""
    g = 7
    p = [
        0.99999999999980993,
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.13857109526572012,
        9.9843695780195716e-6,
        1.5056327351493116e-7,
    ]
    if x < 0.5:
        return math.pi / (math.sin(math.pi * x) * gamma_lanczos(1 - x))
    x -= 1
    a = p[0]
    t = x + g + 0.5
    for i in range(1, g + 2):
        a += p[i] / (x + i)
    return math.sqrt(2 * math.pi) * t ** (x + 0.5) * math.exp(-t) * a


def gamma_stirling(x):
    """Stirling's approximation — less accurate."""
    return math.sqrt(2 * math.pi / x) * (x / math.e) ** x


def benchmark():
    xs = [i * 0.1 + 0.5 for i in range(1, 100)]
    for name, fn in [
        ("math.gamma", gamma_builtin),
        ("lanczos", gamma_lanczos),
        ("stirling", gamma_stirling),
    ]:
        start = time.perf_counter()
        for v in xs:
            fn(v)
        elapsed = (time.perf_counter() - start) * 1000
        sample = fn(5.0)
        print(f"{name:15s} gamma(5)={sample:.6f}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
