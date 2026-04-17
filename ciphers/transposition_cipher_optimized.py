"""
Transposition (Columnar) Cipher — Optimized Variants & Benchmark
=================================================================
Three implementations of columnar transposition encryption.
"""

import math
import timeit


# Variant 1: Original string concatenation
def encrypt_v1(key: int, message: str) -> str:
    cols = [""] * key
    for col in range(key):
        ptr = col
        while ptr < len(message):
            cols[col] += message[ptr]
            ptr += key
    return "".join(cols)


# Variant 2: Slicing via stride
def encrypt_v2(key: int, message: str) -> str:
    return "".join(message[col::key] for col in range(key))


# Variant 3: List-indexed building
def encrypt_v3(key: int, message: str) -> str:
    rows = math.ceil(len(message) / key)
    padded = message.ljust(rows * key)
    return "".join(
        padded[col + row * key] for col in range(key) for row in range(rows)
        if col + row * key < len(message)
    )


def benchmark(n: int = 200_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "msg = 'HARSHIL DARJI WRITES ALGORITHMS' * 5; key = 7"
    )
    t1 = timeit.timeit("encrypt_v1(key, msg)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(key, msg)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(key, msg)", setup=setup, number=n)
    print(f"V1 (string concat): {t1:.4f}s for {n:,} runs")
    print(f"V2 (stride slice) : {t2:.4f}s for {n:,} runs")
    print(f"V3 (list indexed) : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    msg = "HARSHIL DARJI"
    key = 6
    enc1 = encrypt_v1(key, msg)
    enc2 = encrypt_v2(key, msg)
    enc3 = encrypt_v3(key, msg)
    print(f"V1: {enc1}")
    print(f"V2: {enc2}")
    print(f"V3: {enc3}")
    assert enc1 == enc2 == enc3, "Variants disagree!"
    print()
    benchmark()
