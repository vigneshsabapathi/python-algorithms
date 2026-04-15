"""
Primelib optimized — cache primes, sieve-based range, fast totient.
Includes benchmark of totient via factorization vs sieve.
"""
from __future__ import annotations

import math
import time


def sieve(n: int) -> list[int]:
    if n < 2:
        return []
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(math.isqrt(n)) + 1):
        if s[i]:
            s[i * i :: i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i in range(n + 1) if s[i]]


def totient_factor(n: int) -> int:
    r = n
    for p in (2, 3):
        if n % p == 0:
            while n % p == 0:
                n //= p
            r -= r // p
    i = 5
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            r -= r // i
        i += 2
    if n > 1:
        r -= r // n
    return r


def totient_sieve(n: int) -> list[int]:
    """Return phi[0..n] via linear sieve."""
    phi = list(range(n + 1))
    for i in range(2, n + 1):
        if phi[i] == i:  # i is prime
            for j in range(i, n + 1, i):
                phi[j] -= phi[j] // i
    return phi


def benchmark() -> None:
    print(f"{'fn':<20}{'input':>14}{'result':>18}{'ms':>12}")
    for n in (10**3, 10**5, 10**6):
        t = time.perf_counter()
        phis = totient_sieve(n)
        dt = (time.perf_counter() - t) * 1000
        print(f"{'totient_sieve':<20}{n:>14}{phis[n]:>18}{dt:>12.2f}")
    for n in (10**6 - 1, 10**9 + 7, 123456789):
        t = time.perf_counter()
        r = totient_factor(n)
        dt = (time.perf_counter() - t) * 1000
        print(f"{'totient_factor':<20}{n:>14}{r:>18}{dt:>12.4f}")


if __name__ == "__main__":
    benchmark()
