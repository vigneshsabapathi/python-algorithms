"""
Atbash Cipher — Optimized Variants + Benchmark

Three strategies: ord() arithmetic, lookup table, and str.translate.
"""

import string
from timeit import timeit

_LETTERS = string.ascii_letters
_REVERSED = string.ascii_lowercase[::-1] + string.ascii_uppercase[::-1]

# ── Variant 1: generator + index (original fast version) ─────────────────────
def atbash_v1(sequence: str) -> str:
    """Generator using string index lookup."""
    return "".join(
        _REVERSED[_LETTERS.index(c)] if c in _LETTERS else c for c in sequence
    )


# ── Variant 2: ord() arithmetic ──────────────────────────────────────────────
def atbash_v2(sequence: str) -> str:
    """Direct ord() arithmetic: no list construction."""
    out = []
    for c in sequence:
        code = ord(c)
        if 65 <= code <= 90:
            out.append(chr(155 - code))
        elif 97 <= code <= 122:
            out.append(chr(219 - code))
        else:
            out.append(c)
    return "".join(out)


# ── Variant 3: str.translate (fastest for large strings) ─────────────────────
_TABLE = str.maketrans(
    string.ascii_letters,
    string.ascii_lowercase[::-1] + string.ascii_uppercase[::-1],
)


def atbash_v3(sequence: str) -> str:
    """str.translate — O(1) character mapping via C-level table."""
    return sequence.translate(_TABLE)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    sample = (string.printable + "Hello, World! Test 12345") * 20
    n = 100_000

    setup = f"from __main__ import atbash_v1, atbash_v2, atbash_v3; s={sample!r}"
    print("=== Atbash Cipher Benchmark (100k iterations) ===")
    for name, stmt in [
        ("atbash_v1 (index)", "atbash_v1(s)"),
        ("atbash_v2 (ord)", "atbash_v2(s)"),
        ("atbash_v3 (translate)", "atbash_v3(s)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
