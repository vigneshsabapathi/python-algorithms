"""
Rabin-Miller Primality Test — Optimized Variants & Benchmark
=============================================================
Three approaches: probabilistic, deterministic witnesses, and Miller-Rabin
with varying witness counts.
"""

import random
import timeit


LOW_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
    163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
    251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
    349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
    443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 997,
]
LOW_PRIME_SET = set(LOW_PRIMES)


def _miller_rabin_test(n: int, a: int) -> bool:
    """Single Miller-Rabin witness test for *a* against *n*."""
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(r - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


# Variant 1: Probabilistic (5 random witnesses)
def is_prime_v1(n: int) -> bool:
    if n < 2:
        return False
    if n in LOW_PRIME_SET:
        return True
    if any(n % p == 0 for p in LOW_PRIMES):
        return False
    for _ in range(5):
        a = random.randrange(2, n - 1)
        if not _miller_rabin_test(n, a):
            return False
    return True


# Variant 2: Deterministic for n < 3,215,031,751 (fixed witnesses)
WITNESSES_SMALL = [2, 3, 5, 7]


def is_prime_v2(n: int) -> bool:
    if n < 2:
        return False
    if n in LOW_PRIME_SET:
        return True
    if any(n % p == 0 for p in LOW_PRIMES if p < n):
        return False
    for a in WITNESSES_SMALL:
        if a >= n:
            continue
        if not _miller_rabin_test(n, a):
            return False
    return True


# Variant 3: Deterministic for all n < 3,317,044,064,679,887,385,961,981
WITNESSES_LARGE = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


def is_prime_v3(n: int) -> bool:
    if n < 2:
        return False
    if n in LOW_PRIME_SET:
        return True
    if any(n % p == 0 for p in LOW_PRIMES if p < n):
        return False
    for a in WITNESSES_LARGE:
        if a >= n:
            continue
        if not _miller_rabin_test(n, a):
            return False
    return True


def benchmark(n: int = 10_000) -> None:
    candidate = 982_451_653  # a known large prime
    setup = f"from __main__ import is_prime_v1, is_prime_v2, is_prime_v3; c = {candidate}"
    t1 = timeit.timeit("is_prime_v1(c)", setup=setup, number=n)
    t2 = timeit.timeit("is_prime_v2(c)", setup=setup, number=n)
    t3 = timeit.timeit("is_prime_v3(c)", setup=setup, number=n)
    print(f"V1 (5 random)  : {t1:.4f}s for {n:,} runs")
    print(f"V2 (4 fixed)   : {t2:.4f}s for {n:,} runs")
    print(f"V3 (12 fixed)  : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    test_nums = [2, 7, 11, 9, 100, 982_451_653, 982_451_654]
    for num in test_nums:
        print(f"is_prime({num}): V1={is_prime_v1(num)} V2={is_prime_v2(num)} V3={is_prime_v3(num)}")
    print()
    benchmark()
