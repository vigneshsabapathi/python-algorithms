"""
Mono-Alphabetic Cipher — Optimized Variants & Benchmark
=========================================================
"""

import timeit

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# Variant 1: Original character-by-character loop
def encrypt_v1(key: str, message: str) -> str:
    translated = ""
    for s in message:
        if s.upper() in LETTERS:
            idx = LETTERS.find(s.upper())
            translated += key[idx].upper() if s.isupper() else key[idx].lower()
        else:
            translated += s
    return translated


# Variant 2: str.maketrans/translate — single O(n) pass
def encrypt_v2(key: str, message: str) -> str:
    upper_table = str.maketrans(LETTERS, key.upper())
    lower_table = str.maketrans(LETTERS.lower(), key.lower())
    result = ""
    for c in message:
        if c.isupper():
            result += c.translate(upper_table)
        elif c.islower():
            result += c.translate(lower_table)
        else:
            result += c
    return result


# Variant 3: Dict-based lookup
def encrypt_v3(key: str, message: str) -> str:
    fwd = {LETTERS[i]: key[i] for i in range(26)}
    result = ""
    for c in message:
        cu = c.upper()
        if cu in fwd:
            result += fwd[cu].upper() if c.isupper() else fwd[cu].lower()
        else:
            result += c
    return result


def benchmark(n: int = 100_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "key = 'QWERTYUIOPASDFGHJKLZXCVBNM'; msg = 'Hello, this is a test message!'"
    )
    t1 = timeit.timeit("encrypt_v1(key, msg)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(key, msg)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(key, msg)", setup=setup, number=n)
    print(f"V1 (LETTERS.find): {t1:.4f}s for {n:,} runs")
    print(f"V2 (maketrans)   : {t2:.4f}s for {n:,} runs")
    print(f"V3 (dict lookup) : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    msg = "Hello, World!"
    print("V1:", encrypt_v1(key, msg))
    print("V2:", encrypt_v2(key, msg))
    print("V3:", encrypt_v3(key, msg))
    benchmark()
