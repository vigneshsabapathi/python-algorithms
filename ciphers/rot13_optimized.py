"""
ROT13 Cipher — Optimized Variants & Benchmark
===============================================
Three implementations of ROT-n (default 13) rotation.
"""

import timeit


# Variant 1: Explicit char-by-char conditionals
def dencrypt_v1(s: str, n: int = 13) -> str:
    out = ""
    for c in s:
        if "A" <= c <= "Z":
            out += chr(ord("A") + (ord(c) - ord("A") + n) % 26)
        elif "a" <= c <= "z":
            out += chr(ord("a") + (ord(c) - ord("a") + n) % 26)
        else:
            out += c
    return out


# Variant 2: str.maketrans / str.translate (single O(n) pass, no branching)
def dencrypt_v2(s: str, n: int = 13) -> str:
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = upper.lower()
    shifted_upper = upper[n:] + upper[:n]
    shifted_lower = lower[n:] + lower[:n]
    table = str.maketrans(upper + lower, shifted_upper + shifted_lower)
    return s.translate(table)


# Variant 3: codecs rot_13 (only works for n=13)
def dencrypt_v3(s: str, n: int = 13) -> str:
    import codecs
    if n == 13:
        return codecs.encode(s, "rot_13")
    return dencrypt_v1(s, n)  # fallback for other shifts


def benchmark(n: int = 200_000) -> None:
    setup = (
        "from __main__ import dencrypt_v1, dencrypt_v2, dencrypt_v3; "
        "msg = 'The quick brown fox jumps over the lazy dog! 123'"
    )
    t1 = timeit.timeit("dencrypt_v1(msg)", setup=setup, number=n)
    t2 = timeit.timeit("dencrypt_v2(msg)", setup=setup, number=n)
    t3 = timeit.timeit("dencrypt_v3(msg)", setup=setup, number=n)
    print(f"V1 (char loop)    : {t1:.4f}s for {n:,} runs")
    print(f"V2 (maketrans)    : {t2:.4f}s for {n:,} runs")
    print(f"V3 (codecs rot13) : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    msg = "Hello, World!"
    print("V1:", dencrypt_v1(msg))
    print("V2:", dencrypt_v2(msg))
    print("V3:", dencrypt_v3(msg))
    print()
    benchmark()
