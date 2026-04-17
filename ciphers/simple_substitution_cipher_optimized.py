"""
Simple Substitution Cipher — Optimized Variants & Benchmark
=============================================================
"""

import timeit

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# Variant 1: Original character-by-character loop
def encrypt_v1(key: str, message: str) -> str:
    result = ""
    for c in message:
        if c.upper() in LETTERS:
            idx = LETTERS.find(c.upper())
            result += key[idx].upper() if c.isupper() else key[idx].lower()
        else:
            result += c
    return result


# Variant 2: str.maketrans/translate (fastest for large messages)
def encrypt_v2(key: str, message: str) -> str:
    upper_t = str.maketrans(LETTERS, key.upper())
    lower_t = str.maketrans(LETTERS.lower(), key.lower())
    return "".join(
        c.translate(upper_t) if c.isupper() else
        c.translate(lower_t) if c.islower() else c
        for c in message
    )


# Variant 3: Precomputed index array
def encrypt_v3(key: str, message: str) -> str:
    tbl = [key[i] for i in range(26)]
    result: list[str] = []
    for c in message:
        if c.isalpha():
            mapped = tbl[ord(c.upper()) - 65]
            result.append(mapped.upper() if c.isupper() else mapped.lower())
        else:
            result.append(c)
    return "".join(result)


def benchmark(n: int = 100_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "key = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'; "
        "msg = 'The quick brown fox jumps over the lazy dog!'"
    )
    t1 = timeit.timeit("encrypt_v1(key, msg)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(key, msg)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(key, msg)", setup=setup, number=n)
    print(f"V1 (LETTERS.find): {t1:.4f}s for {n:,} runs")
    print(f"V2 (maketrans)   : {t2:.4f}s for {n:,} runs")
    print(f"V3 (index array) : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    key = "LFWOAYUISVKMNXPBDCRJTQEGHZ"
    msg = "Hello, World!"
    print("V1:", encrypt_v1(key, msg))
    print("V2:", encrypt_v2(key, msg))
    print("V3:", encrypt_v3(key, msg))
    benchmark()
