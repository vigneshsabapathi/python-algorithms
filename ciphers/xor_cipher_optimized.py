"""
XOR Cipher — Optimized Variants & Benchmark
=============================================
Three implementations of XOR string encryption.
"""

import timeit


# Variant 1: list comprehension of chr(ord ^ key)
def encrypt_v1(content: str, key: int) -> str:
    key %= 256
    return "".join(chr(ord(c) ^ key) for c in content)


# Variant 2: bytes-level XOR (more idiomatic Python 3)
def encrypt_v2(content: str, key: int) -> str:
    key %= 256
    return bytes(b ^ key for b in content.encode("latin-1")).decode("latin-1")


# Variant 3: bytearray XOR (mutation in-place)
def encrypt_v3(content: str, key: int) -> str:
    key %= 256
    ba = bytearray(content.encode("latin-1"))
    for i in range(len(ba)):
        ba[i] ^= key
    return ba.decode("latin-1")


def benchmark(n: int = 100_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "msg = 'Hello, World! This is a test string.' * 10; key = 42"
    )
    t1 = timeit.timeit("encrypt_v1(msg, key)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(msg, key)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(msg, key)", setup=setup, number=n)
    print(f"V1 (chr/ord list) : {t1:.4f}s for {n:,} runs")
    print(f"V2 (bytes genexpr): {t2:.4f}s for {n:,} runs")
    print(f"V3 (bytearray)    : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    msg = "Hello, World!"
    key = 42
    enc = encrypt_v1(msg, key)
    print("Encrypted:", repr(enc))
    print("Decrypted:", encrypt_v1(enc, key))
    print()
    benchmark()
