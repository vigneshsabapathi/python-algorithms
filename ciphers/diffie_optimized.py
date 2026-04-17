"""
Diffie Primitive Root Finder — Optimized Variants + Benchmark

Three strategies for finding primitive roots modulo a prime.
"""

from timeit import timeit


# ── Variant 1: original list-based check ─────────────────────────────────────
def find_primitive_v1(modulus: int) -> int | None:
    for r in range(1, modulus):
        li = []
        for x in range(modulus - 1):
            val = pow(r, x, modulus)
            if val in li:
                break
            li.append(val)
        else:
            return r
    return None


# ── Variant 2: set-based check (faster membership test) ───────────────────────
def find_primitive_v2(modulus: int) -> int | None:
    for r in range(2, modulus):
        seen: set[int] = set()
        is_primitive = True
        for x in range(modulus - 1):
            val = pow(r, x, modulus)
            if val in seen:
                is_primitive = False
                break
            seen.add(val)
        if is_primitive and len(seen) == modulus - 1:
            return r
    return None


# ── Variant 3: order-based (fastest — uses prime factorization of p-1) ────────
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


def find_primitive_v3(modulus: int) -> int | None:
    """
    Efficient: g is a primitive root iff g^((p-1)/q) != 1 mod p
    for each prime factor q of p-1.
    """
    p_minus_1 = modulus - 1
    factors = _prime_factors(p_minus_1)
    for r in range(2, modulus):
        if all(pow(r, p_minus_1 // f, modulus) != 1 for f in factors):
            return r
    return None


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    primes = [7, 11, 13, 17, 19, 23]
    n = 1_000

    setup = (
        f"from __main__ import find_primitive_v1, find_primitive_v2, find_primitive_v3; "
        f"ps={primes}"
    )
    print("=== Diffie Primitive Root Benchmark (1k iterations over 6 primes) ===")
    for name, stmt in [
        ("v1 (list membership)", "[find_primitive_v1(p) for p in ps]"),
        ("v2 (set membership)", "[find_primitive_v2(p) for p in ps]"),
        ("v3 (factor-based)", "[find_primitive_v3(p) for p in ps]"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
