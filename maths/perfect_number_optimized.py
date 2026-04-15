"""
Optimized Perfect Number checks.

Variants:
  1. naive_half           - iterate i in 1..n//2
  2. sqrt_divisors        - iterate i in 1..sqrt(n), add both divisors
  3. euclid_euler         - uses the Euclid-Euler theorem: every even perfect
                            number has the form 2^(p-1) * (2^p - 1) where
                            (2^p - 1) is a Mersenne prime.
"""
from __future__ import annotations

import math
import time


def naive_half(n: int) -> bool:
    if n <= 1:
        return False
    return sum(i for i in range(1, n // 2 + 1) if n % i == 0) == n


def sqrt_divisors(n: int) -> bool:
    if n <= 1:
        return False
    total = 1  # 1 is always a proper divisor
    r = int(math.isqrt(n))
    for i in range(2, r + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total == n


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True


def euclid_euler(n: int) -> bool:
    """
    Check using the Euclid-Euler theorem for even perfect numbers.

    n must equal 2^(p-1) * (2^p - 1) with (2^p - 1) Mersenne prime.
    """
    if n <= 1 or n % 2 == 1:
        # Odd perfect numbers are unknown; fall back to sqrt method.
        return sqrt_divisors(n)
    # Factor n = 2^(p-1) * m, m odd
    k = n
    p_minus_1 = 0
    while k % 2 == 0:
        k //= 2
        p_minus_1 += 1
    p = p_minus_1 + 1
    mersenne = (1 << p) - 1
    return k == mersenne and _is_prime(mersenne)


def benchmark() -> None:
    numbers = [6, 28, 496, 8128, 33550336]
    funcs = [naive_half, sqrt_divisors, euclid_euler]
    print(f"{'fn':<18}{'n':>12}{'result':>8}{'ms':>12}")
    for fn in funcs:
        for n in numbers:
            if fn is naive_half and n > 100000:
                continue
            t = time.perf_counter()
            r = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<18}{n:>12}{str(r):>8}{dt:>12.4f}")


if __name__ == "__main__":
    benchmark()
