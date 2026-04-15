"""Largest of large a^b — variants + benchmark."""

import math
import time
import random


def compare_log(a1, e1, a2, e2):
    return (e1 * math.log10(a1)) > (e2 * math.log10(a2))


def compare_direct(a1, e1, a2, e2):
    """Only OK when results fit in Python int — always true in Python, but slow for huge exponents."""
    return a1**e1 > a2**e2


def compare_builtin_log(a1, e1, a2, e2):
    return e1 * math.log(a1) > e2 * math.log(a2)


def benchmark():
    pairs = [(random.randint(2, 10), random.randint(100, 500)) for _ in range(1000)]
    for name, fn in [("log10_compare", compare_log), ("ln_compare", compare_builtin_log)]:
        start = time.perf_counter()
        wins = sum(1 for (a, e), (b, f) in zip(pairs[::2], pairs[1::2]) if fn(a, e, b, f))
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} wins={wins}  time={elapsed:.3f} ms")
    # Direct: safe for moderate sizes only
    small = [(random.randint(2, 5), random.randint(10, 30)) for _ in range(1000)]
    start = time.perf_counter()
    wins = sum(1 for (a, e), (b, f) in zip(small[::2], small[1::2]) if compare_direct(a, e, b, f))
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'direct_power':20s} wins={wins}  time={elapsed:.3f} ms (small only)")


if __name__ == "__main__":
    benchmark()
