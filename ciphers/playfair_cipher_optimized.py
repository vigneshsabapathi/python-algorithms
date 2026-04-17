"""
Playfair Cipher — Optimized Variants & Benchmark
=================================================
Three implementations of Playfair encoding.
"""

import itertools
import string
import timeit
from collections.abc import Generator, Iterable


ALPHABET_NJ = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # no J


def _generate_table(key: str) -> list[str]:
    table: list[str] = []
    for c in key.upper():
        if c not in table and c in ALPHABET_NJ:
            table.append(c)
    for c in ALPHABET_NJ:
        if c not in table:
            table.append(c)
    return table


def _prepare(dirty: str) -> str:
    dirty = "".join(c.upper() for c in dirty if c in string.ascii_letters)
    clean = ""
    for i in range(len(dirty) - 1):
        clean += dirty[i]
        if dirty[i] == dirty[i + 1]:
            clean += "X"
    clean += dirty[-1]
    if len(clean) % 2:
        clean += "X"
    return clean


def _chunker(seq: Iterable[str], size: int) -> Generator[tuple[str, ...]]:
    it = iter(seq)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            return
        yield chunk


# Variant 1: List-based table with index lookups
def encode_v1(plaintext: str, key: str) -> str:
    table = _generate_table(key)
    pt = _prepare(plaintext)
    ct = ""
    for c1, c2 in _chunker(pt, 2):
        r1, col1 = divmod(table.index(c1), 5)
        r2, col2 = divmod(table.index(c2), 5)
        if r1 == r2:
            ct += table[r1 * 5 + (col1 + 1) % 5] + table[r2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:
            ct += table[((r1 + 1) % 5) * 5 + col1] + table[((r2 + 1) % 5) * 5 + col2]
        else:
            ct += table[r1 * 5 + col2] + table[r2 * 5 + col1]
    return ct


# Variant 2: Dict-based position lookup (O(1) vs O(n) list.index)
def encode_v2(plaintext: str, key: str) -> str:
    table = _generate_table(key)
    pos = {c: divmod(i, 5) for i, c in enumerate(table)}
    pt = _prepare(plaintext)
    ct = ""
    for c1, c2 in _chunker(pt, 2):
        r1, col1 = pos[c1]
        r2, col2 = pos[c2]
        if r1 == r2:
            ct += table[r1 * 5 + (col1 + 1) % 5] + table[r2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:
            ct += table[((r1 + 1) % 5) * 5 + col1] + table[((r2 + 1) % 5) * 5 + col2]
        else:
            ct += table[r1 * 5 + col2] + table[r2 * 5 + col1]
    return ct


# Variant 3: 5×5 2D list table
def encode_v3(plaintext: str, key: str) -> str:
    flat = _generate_table(key)
    grid = [flat[r * 5 : r * 5 + 5] for r in range(5)]
    pos = {c: (r, col) for r, row in enumerate(grid) for col, c in enumerate(row)}
    pt = _prepare(plaintext)
    ct = ""
    for c1, c2 in _chunker(pt, 2):
        r1, col1 = pos[c1]
        r2, col2 = pos[c2]
        if r1 == r2:
            ct += grid[r1][(col1 + 1) % 5] + grid[r2][(col2 + 1) % 5]
        elif col1 == col2:
            ct += grid[(r1 + 1) % 5][col1] + grid[(r2 + 1) % 5][col2]
        else:
            ct += grid[r1][col2] + grid[r2][col1]
    return ct


def benchmark(n: int = 50_000) -> None:
    setup = (
        "from __main__ import encode_v1, encode_v2, encode_v3; "
        "pt='ATTACK AT DAWN'; key='MONARCHY'"
    )
    t1 = timeit.timeit("encode_v1(pt, key)", setup=setup, number=n)
    t2 = timeit.timeit("encode_v2(pt, key)", setup=setup, number=n)
    t3 = timeit.timeit("encode_v3(pt, key)", setup=setup, number=n)
    print(f"V1 (list.index): {t1:.4f}s for {n:,} runs")
    print(f"V2 (dict pos)  : {t2:.4f}s for {n:,} runs")
    print(f"V3 (2D grid)   : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    print("V1:", encode_v1("ATTACK AT DAWN", "MONARCHY"))
    print("V2:", encode_v2("ATTACK AT DAWN", "MONARCHY"))
    print("V3:", encode_v3("ATTACK AT DAWN", "MONARCHY"))
    print()
    benchmark()
