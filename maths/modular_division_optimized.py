"""Modular division — variants + benchmark."""

import math
import time
import random


def ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = ext_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def mod_inv_extgcd(a, m):
    g, x, _ = ext_gcd(a % m, m)
    if g != 1:
        raise ValueError("no inverse")
    return x % m


def mod_inv_fermat(a, p):
    """Only works when p is prime."""
    return pow(a, p - 2, p)


def mod_inv_builtin(a, m):
    return pow(a, -1, m)  # Python 3.8+


def benchmark():
    p = 10**9 + 7  # prime
    values = [random.randint(1, p - 1) for _ in range(10_000)]
    for name, fn in [
        ("extended_gcd", lambda: [mod_inv_extgcd(v, p) for v in values]),
        ("fermat_pow", lambda: [mod_inv_fermat(v, p) for v in values]),
        ("pow_builtin_neg1", lambda: [mod_inv_builtin(v, p) for v in values]),
    ]:
        start = time.perf_counter()
        fn()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:22s} time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
