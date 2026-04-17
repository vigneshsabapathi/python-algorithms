"""
ElGamal Key Generator — Optimized Variants + Benchmark

Three primitive root strategies: random trial, factor-based (correct),
and small prime sieve.
"""

import random
from timeit import timeit

from ciphers.deterministic_miller_rabin import miller_rabin


def _is_prime(n: int) -> bool:
    return miller_rabin(n, allow_probable=True)


def _prime_factors(n: int) -> list[int]:
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


# ── Variant 1: random trial (original heuristic) ──────────────────────────────
def primitive_root_v1(p: int) -> int:
    while True:
        g = random.randrange(3, p)
        if pow(g, 2, p) == 1:
            continue
        if pow(g, p, p) == 1:
            continue
        return g


# ── Variant 2: factor-based (correct, Handbook Algorithm 4.80) ────────────────
def primitive_root_v2(p: int) -> int:
    p_minus_1 = p - 1
    factors = _prime_factors(p_minus_1)
    while True:
        g = random.randint(2, p - 1)
        if all(pow(g, p_minus_1 // f, p) != 1 for f in factors):
            return g


# ── Variant 3: smallest primitive root (deterministic, no randomness) ─────────
def primitive_root_v3(p: int) -> int:
    """Return the smallest primitive root mod p."""
    p_minus_1 = p - 1
    factors = _prime_factors(p_minus_1)
    for g in range(2, p):
        if all(pow(g, p_minus_1 // f, p) != 1 for f in factors):
            return g
    return -1


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    # Use a small prime for fast benchmarking
    p = 104729  # prime
    n = 1_000

    setup = (
        f"from __main__ import primitive_root_v1, primitive_root_v2, primitive_root_v3; "
        f"p={p}"
    )
    print("=== ElGamal Primitive Root Benchmark (1k iterations, p=104729) ===")
    for name, stmt in [
        ("v1 (random heuristic)", "primitive_root_v1(p)"),
        ("v2 (factor-based random)", "primitive_root_v2(p)"),
        ("v3 (smallest, deterministic)", "primitive_root_v3(p)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
