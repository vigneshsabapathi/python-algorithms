"""Square-free — variants + benchmark."""

import time
import random


def sf_trial_squares(n):
    if n < 1:
        return False
    if n == 1:
        return True
    if n % 4 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % (i * i) == 0:
            return False
        i += 2
    return True


def sf_factorize(n):
    if n == 1:
        return True
    i = 2
    while i * i <= n:
        if n % i == 0:
            n //= i
            if n % i == 0:
                return False
            i += 1 if i == 2 else 2
        else:
            i += 1 if i == 2 else 2
    return True


def sf_sieve_build(limit):
    """Precompute square-free flags up to limit."""
    sf = [True] * (limit + 1)
    sf[0] = False
    i = 2
    while i * i <= limit:
        sq = i * i
        for j in range(sq, limit + 1, sq):
            sf[j] = False
        i += 1
    return sf


def benchmark():
    nums = [random.randint(1, 10**9) for _ in range(5000)]
    for name, fn in [("trial_squares", sf_trial_squares), ("factorize", sf_factorize)]:
        start = time.perf_counter()
        hits = sum(1 for v in nums if fn(v))
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:18s} sf_count={hits}  time={elapsed:.3f} ms")
    N = 1_000_000
    start = time.perf_counter()
    sf = sf_sieve_build(N)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'sieve_precompute':18s} N={N} count={sum(sf)}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
