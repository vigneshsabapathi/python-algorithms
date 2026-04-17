"""
Cryptomath Module — Optimized Variants + Benchmark

Three approaches for modular multiplicative inverse:
extended Euclidean, pow(a, -1, m) (Python 3.8+), and Fermat's little theorem.
"""

from math import gcd
from timeit import timeit


# ── Variant 1: extended Euclidean (original) ──────────────────────────────────
def find_mod_inverse_v1(a: int, m: int) -> int:
    if gcd(a, m) != 1:
        raise ValueError(f"mod inverse of {a} and {m} does not exist")
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = u1 - q*v1, u2 - q*v2, u3 - q*v3, v1, v2, v3
    return u1 % m


# ── Variant 2: Python 3.8+ built-in pow(a, -1, m) ────────────────────────────
def find_mod_inverse_v2(a: int, m: int) -> int:
    """Uses Python's built-in modular inverse (fastest for large numbers)."""
    try:
        return pow(a, -1, m)
    except ValueError:
        raise ValueError(f"mod inverse of {a} and {m} does not exist")


# ── Variant 3: Fermat's little theorem (only valid when m is prime) ───────────
def find_mod_inverse_v3_prime_modulus(a: int, p: int) -> int:
    """Valid only when p is prime: a^(p-2) mod p == a^-1 mod p."""
    if gcd(a, p) != 1:
        raise ValueError(f"mod inverse of {a} and {p} does not exist")
    return pow(a, p - 2, p)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    a, m = 7, 26
    a_large, m_prime = 123456789, 999999937  # m_prime is prime
    n = 500_000

    setup = (
        f"from __main__ import find_mod_inverse_v1, find_mod_inverse_v2, "
        f"find_mod_inverse_v3_prime_modulus; "
        f"a={a}; m={m}; al={a_large}; mp={m_prime}"
    )
    print("=== Cryptomath Benchmark (500k iterations, small inputs) ===")
    for name, stmt in [
        ("v1 ext Euclidean (a=7,m=26)", "find_mod_inverse_v1(a, m)"),
        ("v2 pow(a,-1,m) (a=7,m=26)", "find_mod_inverse_v2(a, m)"),
        ("v1 ext Euclidean (large)", "find_mod_inverse_v1(al, mp)"),
        ("v2 pow(a,-1,m) (large)", "find_mod_inverse_v2(al, mp)"),
        ("v3 Fermat (prime m, large)", "find_mod_inverse_v3_prime_modulus(al, mp)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
