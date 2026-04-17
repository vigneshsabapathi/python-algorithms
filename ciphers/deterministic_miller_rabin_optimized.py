"""
Miller-Rabin Primality Test — Optimized Variants + Benchmark

Three strategies: original witness loop, sympy.isprime (if available),
and a quick sieve shortcut for small numbers.
"""

from timeit import timeit

# Small primes sieve for fast rejection
_SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

BOUNDS = [
    2_047, 1_373_653, 25_326_001, 3_215_031_751,
    2_152_302_898_747, 3_474_749_660_383, 341_550_071_728_321, 1,
    3_825_123_056_546_413_051, 1, 1,
    318_665_857_834_031_151_167_461, 3_317_044_064_679_887_385_961_981,
]
WITNESSES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]


# ── Variant 1: original deterministic ────────────────────────────────────────
def miller_rabin_v1(n: int, allow_probable: bool = False) -> bool:
    if n == 2:
        return True
    if not n % 2 or n < 2:
        return False
    if n > 5 and n % 10 not in (1, 3, 7, 9):
        return False
    if n > 3_317_044_064_679_887_385_961_981 and not allow_probable:
        raise ValueError("Exceeds deterministic bound. Use allow_probable=True.")
    for idx, bound in enumerate(BOUNDS, 1):
        if n < bound:
            plist = WITNESSES[:idx]
            break
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for prime in plist:
        pr = False
        for r in range(s):
            m = pow(prime, d * 2**r, n)
            if (r == 0 and m == 1) or ((m + 1) % n == 0):
                pr = True
                break
        if not pr:
            return False
    return True


# ── Variant 2: with small-prime fast path ────────────────────────────────────
def miller_rabin_v2(n: int) -> bool:
    """Adds small-prime divisibility check before Miller-Rabin."""
    if n < 2:
        return False
    for p in _SMALL_PRIMES:
        if n == p:
            return True
        if n % p == 0:
            return False
    return miller_rabin_v1(n)


# ── Variant 3: using sympy if available, else fallback ────────────────────────
def miller_rabin_v3(n: int) -> bool:
    try:
        from sympy import isprime
        return isprime(n)
    except ImportError:
        return miller_rabin_v1(n)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    test_numbers = [838_207, 563, 17_316_017, 3_078_386_653, 1_713_045_574_819]
    n = 10_000

    setup = (
        f"from __main__ import miller_rabin_v1, miller_rabin_v2, miller_rabin_v3; "
        f"nums={test_numbers}"
    )
    print("=== Miller-Rabin Benchmark (10k iterations over 5 primes) ===")
    for name, stmt in [
        ("v1 (original)", "[miller_rabin_v1(x) for x in nums]"),
        ("v2 (small prime shortcut)", "[miller_rabin_v2(x) for x in nums]"),
        ("v3 (sympy fallback)", "[miller_rabin_v3(x) for x in nums]"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
