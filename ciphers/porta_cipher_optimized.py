"""
Porta Cipher — Optimized Variants & Benchmark
===============================================
Three implementations of Porta encryption.
"""

import timeit

ALPHABET: dict[str, tuple[str, str]] = {
    "A": ("ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"),
    "B": ("ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"),
    "C": ("ABCDEFGHIJKLM", "ZNOPQRSTUVWXY"),
    "D": ("ABCDEFGHIJKLM", "ZNOPQRSTUVWXY"),
    "E": ("ABCDEFGHIJKLM", "YZNOPQRSTUVWX"),
    "F": ("ABCDEFGHIJKLM", "YZNOPQRSTUVWX"),
    "G": ("ABCDEFGHIJKLM", "XYZNOPQRSTUVW"),
    "H": ("ABCDEFGHIJKLM", "XYZNOPQRSTUVW"),
    "I": ("ABCDEFGHIJKLM", "WXYZNOPQRSTUV"),
    "J": ("ABCDEFGHIJKLM", "WXYZNOPQRSTUV"),
    "K": ("ABCDEFGHIJKLM", "VWXYZNOPQRSTU"),
    "L": ("ABCDEFGHIJKLM", "VWXYZNOPQRSTU"),
    "M": ("ABCDEFGHIJKLM", "UVWXYZNOPQRST"),
    "N": ("ABCDEFGHIJKLM", "UVWXYZNOPQRST"),
    "O": ("ABCDEFGHIJKLM", "TUVWXYZNOPQRS"),
    "P": ("ABCDEFGHIJKLM", "TUVWXYZNOPQRS"),
    "Q": ("ABCDEFGHIJKLM", "STUVWXYZNOPQR"),
    "R": ("ABCDEFGHIJKLM", "STUVWXYZNOPQR"),
    "S": ("ABCDEFGHIJKLM", "RSTUVWXYZNOPQ"),
    "T": ("ABCDEFGHIJKLM", "RSTUVWXYZNOPQ"),
    "U": ("ABCDEFGHIJKLM", "QRSTUVWXYZNOP"),
    "V": ("ABCDEFGHIJKLM", "QRSTUVWXYZNOP"),
    "W": ("ABCDEFGHIJKLM", "PQRSTUVWXYZNO"),
    "X": ("ABCDEFGHIJKLM", "PQRSTUVWXYZNO"),
    "Y": ("ABCDEFGHIJKLM", "OPQRSTUVWXYZN"),
    "Z": ("ABCDEFGHIJKLM", "OPQRSTUVWXYZN"),
}


# Variant 1: Original table-list approach
def encrypt_v1(key: str, text: str) -> str:
    table = [ALPHABET[c] for c in key.upper()]
    result = ""
    for i, c in enumerate(text.upper()):
        t = table[i % len(table)]
        row = 0 if c in t[0] else 1
        col = t[row].index(c)
        result += t[1 - row][col]
    return result


# Variant 2: Dict-based position precomputation
def encrypt_v2(key: str, text: str) -> str:
    table = [ALPHABET[c] for c in key.upper()]
    # Precompute char->opponent for each table entry
    maps = []
    for t in table:
        m: dict[str, str] = {}
        for col, (c0, c1) in enumerate(zip(t[0], t[1])):
            m[c0] = c1
            m[c1] = c0
        maps.append(m)
    klen = len(maps)
    return "".join(maps[i % klen].get(c, c) for i, c in enumerate(text.upper()))


# Variant 3: Precompute full cipher table as list of 26-char mappings
def encrypt_v3(key: str, text: str) -> str:
    table = [ALPHABET[c] for c in key.upper()]
    all_maps = []
    for t in table:
        combined = t[0] + t[1]  # 26 chars
        forward = {combined[i]: combined[(i + 13) % 26] for i in range(26)}
        all_maps.append(forward)
    klen = len(all_maps)
    return "".join(all_maps[i % klen].get(c, c) for i, c in enumerate(text.upper()))


def benchmark(n: int = 100_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "key = 'marvin'; msg = 'JESSICA'"
    )
    t1 = timeit.timeit("encrypt_v1(key, msg)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(key, msg)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(key, msg)", setup=setup, number=n)
    print(f"V1 (table.index)  : {t1:.4f}s for {n:,} runs")
    print(f"V2 (dict opponent): {t2:.4f}s for {n:,} runs")
    print(f"V3 (26-char map)  : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    key, msg = "marvin", "jessica"
    print("V1:", encrypt_v1(key, msg))
    print("V2:", encrypt_v2(key, msg))
    print("V3:", encrypt_v3(key, msg))
    benchmark()
