"""
RSA Key Generator — Optimized Variants & Benchmark
====================================================
Three approaches to computing the modular inverse (critical inner loop).
"""

import math
import random
import timeit

from ciphers.rabin_miller import generate_large_prime


# Variant 1: Extended Euclidean (iterative)
def mod_inverse_v1(a: int, m: int) -> int:
    if math.gcd(a, m) != 1:
        raise ValueError(f"{a} and {m} are not coprime")
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        u1, u2, u3, v1, v2, v3 = v1, v2, v3, u1 - q * v1, u2 - q * v2, u3 - q * v3
    return u1 % m


# Variant 2: Python 3.8+ pow(a, -1, m)
def mod_inverse_v2(a: int, m: int) -> int:
    return pow(a, -1, m)


# Variant 3: Recursive extended Euclidean
def mod_inverse_v3(a: int, m: int) -> int:
    def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} and {m} are not coprime")
    return x % m


def generate_key_pair(key_size: int) -> tuple[tuple[int, int], tuple[int, int]]:
    p = generate_large_prime(key_size)
    q = generate_large_prime(key_size)
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randrange(2 ** (key_size - 1), 2**key_size)
        if math.gcd(e, phi) == 1:
            break
    d = mod_inverse_v2(e, phi)
    return (n, e), (n, d)


def benchmark(n: int = 100_000) -> None:
    a, m = 17, 3120  # small values for timing
    setup = f"from __main__ import mod_inverse_v1, mod_inverse_v2, mod_inverse_v3; a={a}; m={m}"
    t1 = timeit.timeit("mod_inverse_v1(a, m)", setup=setup, number=n)
    t2 = timeit.timeit("mod_inverse_v2(a, m)", setup=setup, number=n)
    t3 = timeit.timeit("mod_inverse_v3(a, m)", setup=setup, number=n)
    print(f"V1 (iter ext-gcd) : {t1:.4f}s for {n:,} runs")
    print(f"V2 (pow builtin)  : {t2:.4f}s for {n:,} runs")
    print(f"V3 (recur ext-gcd): {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    print("mod_inverse(17, 3120) =", mod_inverse_v1(17, 3120))
    print("mod_inverse(17, 3120) =", mod_inverse_v2(17, 3120))
    print("mod_inverse(17, 3120) =", mod_inverse_v3(17, 3120))
    benchmark()
