"""
RSA Factorization — Optimized Variants & Benchmark
====================================================
Three approaches to recovering p, q from (d, e, n).
"""

import math
import random
import timeit


# Variant 1: Original (iterative t//=2 with gcd)
def rsafactor_v1(d: int, e: int, n: int) -> list[int]:
    k = d * e - 1
    p = 0
    while p == 0:
        g = random.randint(2, n - 1)
        t = k
        while True:
            if t % 2 == 0:
                t //= 2
                x = pow(g, t, n)
                y = math.gcd(x - 1, n)
                if x > 1 and y > 1:
                    p = y
                    break
            else:
                break
    return sorted([p, n // p])


# Variant 2: Batch random choices (avoids recomputing k on each retry)
def rsafactor_v2(d: int, e: int, n: int) -> list[int]:
    k = d * e - 1
    # precompute the trail of halved values from k
    halves: list[int] = []
    tmp = k
    while tmp % 2 == 0:
        tmp //= 2
        halves.append(tmp)
    for _ in range(1000):  # bounded retries
        g = random.randint(2, n - 1)
        for t in halves:
            x = pow(g, t, n)
            y = math.gcd(x - 1, n)
            if 1 < y < n:
                return sorted([y, n // y])
    return []  # extremely unlikely to reach here


# Variant 3: Pollard's p-1 algorithm (different factoring strategy)
def rsafactor_v3(d: int, e: int, n: int) -> list[int]:
    """Fallback: Pollard's p-1 for smooth primes."""
    a = 2
    for j in range(2, 100):
        a = pow(a, j, n)
        g = math.gcd(a - 1, n)
        if 1 < g < n:
            return sorted([g, n // g])
    # If Pollard's p-1 fails, fall back to v1
    return rsafactor_v1(d, e, n)


def benchmark(n: int = 1000) -> None:
    # Small textbook example that resolves instantly
    setup = "from __main__ import rsafactor_v1, rsafactor_v2; d=3; e=16971; n=25777"
    t1 = timeit.timeit("rsafactor_v1(d, e, n)", setup=setup, number=n)
    t2 = timeit.timeit("rsafactor_v2(d, e, n)", setup=setup, number=n)
    print(f"V1 (original)     : {t1:.4f}s for {n:,} runs")
    print(f"V2 (precomp halvs): {t2:.4f}s for {n:,} runs")


if __name__ == "__main__":
    d, e, n = 3, 16971, 25777
    print("V1:", rsafactor_v1(d, e, n))
    print("V2:", rsafactor_v2(d, e, n))
    print("V3:", rsafactor_v3(d, e, n))
    print()
    benchmark()
