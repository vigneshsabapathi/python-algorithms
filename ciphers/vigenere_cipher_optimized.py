"""
Vigenère Cipher — Optimized Variants & Benchmark
=================================================
Three implementations of Vigenère encryption/decryption.
"""

import timeit

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# Variant 1: Original character-by-character with modulo
def encrypt_v1(key: str, message: str) -> str:
    key = key.upper()
    ki = 0
    result: list[str] = []
    for c in message:
        n = LETTERS.find(c.upper())
        if n != -1:
            n = (n + LETTERS.find(key[ki % len(key)])) % 26
            result.append(LETTERS[n] if c.isupper() else LETTERS[n].lower())
            ki += 1
        else:
            result.append(c)
    return "".join(result)


# Variant 2: ordinal arithmetic (avoids LETTERS.find overhead)
def encrypt_v2(key: str, message: str) -> str:
    key = key.upper()
    key_ords = [ord(k) - 65 for k in key]
    klen = len(key)
    ki = 0
    result: list[str] = []
    for c in message:
        cu = c.upper()
        if "A" <= cu <= "Z":
            n = (ord(cu) - 65 + key_ords[ki % klen]) % 26
            result.append(chr(n + 65) if c.isupper() else chr(n + 97))
            ki += 1
        else:
            result.append(c)
    return "".join(result)


# Variant 3: precomputed key cycle with itertools
def encrypt_v3(key: str, message: str) -> str:
    import itertools
    key_cycle = itertools.cycle(ord(k) - 65 for k in key.upper())
    result: list[str] = []
    for c in message:
        cu = c.upper()
        if "A" <= cu <= "Z":
            shift = next(key_cycle)
            n = (ord(cu) - 65 + shift) % 26
            result.append(chr(n + 65) if c.isupper() else chr(n + 97))
        else:
            result.append(c)
    return "".join(result)


def benchmark(n: int = 100_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "key='LEMON'; msg='Attack at dawn, retreat at dusk!'"
    )
    t1 = timeit.timeit("encrypt_v1(key, msg)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(key, msg)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(key, msg)", setup=setup, number=n)
    print(f"V1 (LETTERS.find) : {t1:.4f}s for {n:,} runs")
    print(f"V2 (ord arith)    : {t2:.4f}s for {n:,} runs")
    print(f"V3 (itertools)    : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    key, msg = "LEMON", "Attack at dawn!"
    print("V1:", encrypt_v1(key, msg))
    print("V2:", encrypt_v2(key, msg))
    print("V3:", encrypt_v3(key, msg))
    print()
    benchmark()
