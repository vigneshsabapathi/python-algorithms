"""Möbius function — variants + benchmark."""

import time


def mobius_trial(n):
    if n == 1:
        return 1
    count = 0
    i = 2
    while i * i <= n:
        if n % i == 0:
            n //= i
            if n % i == 0:
                return 0
            count += 1
        i += 1
    if n > 1:
        count += 1
    return -1 if count % 2 else 1


def mobius_sieve(limit):
    """Linear sieve computing μ[1..limit]."""
    mu = [0] * (limit + 1)
    mu[1] = 1
    primes = []
    is_comp = [False] * (limit + 1)
    for i in range(2, limit + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            if i * p > limit:
                break
            is_comp[i * p] = True
            if i % p == 0:
                mu[i * p] = 0
                break
            else:
                mu[i * p] = -mu[i]
    return mu


def mobius_eratosthenes(limit):
    """Simpler sieve — slower but clearer."""
    mu = [1] * (limit + 1)
    mu[0] = 0
    for p in range(2, limit + 1):
        if mu[p] == 1 or mu[p] == -1:
            # not yet flipped, but still might be; detect prime by checking
            pass
    # Use standard sieve approach:
    mu = [1] * (limit + 1)
    mu[0] = 0
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    for i in range(2, limit + 1):
        if prime[i]:
            for j in range(i, limit + 1, i):
                if j > i:
                    prime[j] = False
                mu[j] *= -1
            sq = i * i
            for j in range(sq, limit + 1, sq):
                mu[j] = 0
    return mu


def benchmark():
    N = 100_000
    start = time.perf_counter()
    bulk = [mobius_trial(i) for i in range(1, N + 1)]
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'trial_bulk':18s} sum={sum(bulk)}  time={elapsed:.3f} ms")

    start = time.perf_counter()
    tbl = mobius_sieve(N)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'linear_sieve':18s} sum={sum(tbl[1:])}  time={elapsed:.3f} ms")

    start = time.perf_counter()
    tbl2 = mobius_eratosthenes(N)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'eratosthenes_sieve':18s} sum={sum(tbl2[1:])}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
