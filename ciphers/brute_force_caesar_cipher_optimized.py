"""
Brute-Force Caesar Cipher — Optimized Variants + Benchmark

Three strategies for generating all 26 decryptions.
"""

import string
from timeit import timeit

_UPPER = string.ascii_uppercase
_LEN = len(_UPPER)


# ── Variant 1: nested for-loop (original) ────────────────────────────────────
def brute_force_v1(message: str) -> dict[int, str]:
    results = {}
    for key in range(_LEN):
        translated = ""
        for sym in message:
            if sym in _UPPER:
                translated += _UPPER[((_UPPER.find(sym)) - key) % _LEN]
            else:
                translated += sym
        results[key] = translated
    return results


# ── Variant 2: str.translate per key ─────────────────────────────────────────
def brute_force_v2(message: str) -> dict[int, str]:
    results = {}
    for key in range(_LEN):
        table = str.maketrans(
            _UPPER,
            _UPPER[key:] + _UPPER[:key],
        )
        results[key] = message.translate(table)
    return results


# ── Variant 3: precompute shifted alphabets ───────────────────────────────────
_SHIFTED = [_UPPER[k:] + _UPPER[:k] for k in range(_LEN)]
_TABLES = [str.maketrans(_UPPER, s) for s in _SHIFTED]


def brute_force_v3(message: str) -> dict[int, str]:
    return {key: message.translate(_TABLES[key]) for key in range(_LEN)}


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    msg = "TMDETUX PMDVU THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    n = 20_000

    setup = (
        f"from __main__ import brute_force_v1, brute_force_v2, brute_force_v3; "
        f"m={msg!r}"
    )
    print("=== Brute Force Caesar Benchmark (20k iterations) ===")
    for name, stmt in [
        ("brute_force_v1 (nested loop)", "brute_force_v1(m)"),
        ("brute_force_v2 (translate per key)", "brute_force_v2(m)"),
        ("brute_force_v3 (precomputed tables)", "brute_force_v3(m)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
