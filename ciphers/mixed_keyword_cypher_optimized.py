"""
Mixed Keyword Cipher — Optimized Variants & Benchmark
======================================================
Three implementation approaches compared with timeit.
"""

import timeit
from string import ascii_uppercase


# ---------------------------------------------------------------------------
# Variant 1: Original columnar-grid approach (reference implementation)
# ---------------------------------------------------------------------------
def mixed_keyword_v1(keyword: str, plaintext: str) -> str:
    """Column-read grid mapping — faithful to the original algorithm."""
    keyword = keyword.upper()
    plaintext = plaintext.upper()
    unique = list(dict.fromkeys(c for c in keyword if c in ascii_uppercase))
    num_cols = len(unique)
    shifted = unique + [c for c in ascii_uppercase if c not in unique]
    rows = [shifted[k : k + num_cols] for k in range(0, 26, num_cols)]
    mapping: dict[str, str] = {}
    idx = 0
    for col in range(num_cols):
        for row in rows:
            if len(row) <= col:
                break
            mapping[ascii_uppercase[idx]] = row[col]
            idx += 1
    return "".join(mapping.get(c, c) for c in plaintext)


# ---------------------------------------------------------------------------
# Variant 2: Pre-built translation table using str.maketrans / str.translate
# ---------------------------------------------------------------------------
def mixed_keyword_v2(keyword: str, plaintext: str) -> str:
    """Uses str.maketrans/translate for O(1) per-character lookup after setup."""
    keyword = keyword.upper()
    unique = list(dict.fromkeys(c for c in keyword if c in ascii_uppercase))
    num_cols = len(unique)
    shifted = unique + [c for c in ascii_uppercase if c not in unique]
    rows = [shifted[k : k + num_cols] for k in range(0, 26, num_cols)]
    plain_chars: list[str] = []
    cipher_chars: list[str] = []
    idx = 0
    for col in range(num_cols):
        for row in rows:
            if len(row) <= col:
                break
            plain_chars.append(ascii_uppercase[idx])
            cipher_chars.append(row[col])
            idx += 1
    table = str.maketrans("".join(plain_chars), "".join(cipher_chars))
    return plaintext.upper().translate(table)


# ---------------------------------------------------------------------------
# Variant 3: Precomputed index array (numpy-style, pure Python)
# ---------------------------------------------------------------------------
def mixed_keyword_v3(keyword: str, plaintext: str) -> str:
    """Direct ordinal array lookup — avoids dict overhead entirely."""
    keyword = keyword.upper()
    unique = list(dict.fromkeys(c for c in keyword if c in ascii_uppercase))
    num_cols = len(unique)
    shifted = unique + [c for c in ascii_uppercase if c not in unique]
    rows = [shifted[k : k + num_cols] for k in range(0, 26, num_cols)]
    cipher_ord = [0] * 26  # cipher_ord[i] = ord of encrypted letter for alphabet[i]
    idx = 0
    for col in range(num_cols):
        for row in rows:
            if len(row) <= col:
                break
            cipher_ord[idx] = ord(row[col])
            idx += 1
    return "".join(
        chr(cipher_ord[ord(c) - 65]) if c.isalpha() else c
        for c in plaintext.upper()
    )


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(n: int = 100_000) -> None:
    setup = "from __main__ import mixed_keyword_v1, mixed_keyword_v2, mixed_keyword_v3"
    stmt1 = "mixed_keyword_v1('college', 'UNIVERSITY CHALLENGE')"
    stmt2 = "mixed_keyword_v2('college', 'UNIVERSITY CHALLENGE')"
    stmt3 = "mixed_keyword_v3('college', 'UNIVERSITY CHALLENGE')"
    t1 = timeit.timeit(stmt1, setup=setup, number=n)
    t2 = timeit.timeit(stmt2, setup=setup, number=n)
    t3 = timeit.timeit(stmt3, setup=setup, number=n)
    print(f"V1 (grid+dict)    : {t1:.4f}s for {n:,} runs")
    print(f"V2 (maketrans)    : {t2:.4f}s for {n:,} runs")
    print(f"V3 (ordinal array): {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    print(mixed_keyword_v1("college", "UNIVERSITY"))
    print(mixed_keyword_v2("college", "UNIVERSITY"))
    print(mixed_keyword_v3("college", "UNIVERSITY"))
    print()
    benchmark()
