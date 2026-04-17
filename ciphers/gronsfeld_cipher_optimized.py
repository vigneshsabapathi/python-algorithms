"""
Gronsfeld Cipher — Optimized Variants + Benchmark

Three encryption strategies: index + modulo, ord() arithmetic, str.translate per key.
"""

from string import ascii_uppercase
from timeit import timeit


# ── Variant 1: original index-based ──────────────────────────────────────────
def gronsfeld_v1(text: str, key: str) -> str:
    key_ints = [int(c) for c in key]
    key_len = len(key_ints)
    out = []
    ki = 0
    for ch in text.upper():
        if ch in ascii_uppercase:
            out.append(ascii_uppercase[(ascii_uppercase.index(ch) + key_ints[ki % key_len]) % 26])
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


# ── Variant 2: ord() arithmetic ──────────────────────────────────────────────
def gronsfeld_v2(text: str, key: str) -> str:
    key_ints = [int(c) for c in key]
    key_len = len(key_ints)
    out = []
    ki = 0
    for ch in text.upper():
        code = ord(ch)
        if 65 <= code <= 90:
            out.append(chr((code - 65 + key_ints[ki % key_len]) % 26 + 65))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


# ── Variant 3: precompute per-shift translate table ───────────────────────────
_SHIFT_TABLES = {
    d: str.maketrans(ascii_uppercase, ascii_uppercase[d:] + ascii_uppercase[:d])
    for d in range(10)
}


def gronsfeld_v3(text: str, key: str) -> str:
    """Per-character translate call — efficient for digit keys 0-9."""
    key_ints = [int(c) for c in key]
    key_len = len(key_ints)
    out = []
    ki = 0
    for ch in text.upper():
        if ch in ascii_uppercase:
            out.append(ch.translate(_SHIFT_TABLES[key_ints[ki % key_len]]))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    msg = "the quick brown fox jumps over the lazy dog " * 5
    key = "31415"
    n = 50_000

    setup = (
        f"from __main__ import gronsfeld_v1, gronsfeld_v2, gronsfeld_v3; "
        f"m={msg!r}; k={key!r}"
    )
    print("=== Gronsfeld Cipher Benchmark (50k iterations) ===")
    for name, stmt in [
        ("gronsfeld_v1 (index)", "gronsfeld_v1(m, k)"),
        ("gronsfeld_v2 (ord)", "gronsfeld_v2(m, k)"),
        ("gronsfeld_v3 (translate)", "gronsfeld_v3(m, k)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
