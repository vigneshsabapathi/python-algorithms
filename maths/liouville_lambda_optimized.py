"""Liouville λ — variants + benchmark."""

import time


def big_omega_trial(n):
    c = 0
    i = 2
    while i * i <= n:
        while n % i == 0:
            n //= i
            c += 1
        i += 1
    if n > 1:
        c += 1
    return c


def liouville_trial(n):
    return 1 if big_omega_trial(n) % 2 == 0 else -1


def liouville_table(limit):
    """Precompute λ for all 1..limit via sieve on smallest prime factor."""
    spf = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if spf[i] == 0:
            for j in range(i, limit + 1, i):
                if spf[j] == 0:
                    spf[j] = i
    lam = [0] * (limit + 1)
    lam[1] = 1
    for i in range(2, limit + 1):
        p = spf[i]
        lam[i] = -lam[i // p]
    return lam


def liouville_sieve_full(limit):
    """Alternative: sieve Ω(n) directly."""
    omega = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if omega[i] == 0:  # prime
            pk = i
            while pk <= limit:
                for j in range(pk, limit + 1, pk):
                    omega[j] += 1
                if pk > limit // i:
                    break
                pk *= i
    return [1 if omega[i] % 2 == 0 else -1 for i in range(limit + 1)]


def benchmark():
    N = 100_000
    start = time.perf_counter()
    bulk_trial = [liouville_trial(i) for i in range(1, N + 1)]
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'trial_bulk':20s} sum={sum(bulk_trial)}  time={elapsed:.3f} ms")

    start = time.perf_counter()
    tbl = liouville_table(N)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'sieve_spf_recur':20s} sum={sum(tbl[1:])}  time={elapsed:.3f} ms")

    start = time.perf_counter()
    tbl2 = liouville_sieve_full(N)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'sieve_omega':20s} sum={sum(tbl2[1:])}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
