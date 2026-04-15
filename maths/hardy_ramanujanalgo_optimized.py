"""Hardy-Ramanujan omega(n) — variants + benchmark."""

import time


def omega_trial(n):
    count = 0
    if n % 2 == 0:
        count += 1
        while n % 2 == 0:
            n //= 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            count += 1
            while n % i == 0:
                n //= i
        i += 2
    if n > 1:
        count += 1
    return count


def omega_set(n):
    factors = set()
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 1
    if n > 1:
        factors.add(n)
    return len(factors)


def omega_sieve_build(limit):
    """Precompute omega for all [0, limit] — amortized best for many queries."""
    omega = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if omega[i] == 0:  # i is prime
            for j in range(i, limit + 1, i):
                omega[j] += 1
    return omega


def benchmark():
    N = 200_000
    # Single n test: use large
    big = 999_999_937 * 2  # huge semiprime-ish
    for name, fn in [("trial_div", omega_trial), ("set_based", omega_set)]:
        start = time.perf_counter()
        for i in range(2, 10_000):
            fn(i)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} bulk 10k  time={elapsed:.3f} ms")
    start = time.perf_counter()
    table = omega_sieve_build(N)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'sieve_precompute':20s} N={N}  time={elapsed:.3f} ms  omega(2520)={table[2520]}")


if __name__ == "__main__":
    benchmark()
