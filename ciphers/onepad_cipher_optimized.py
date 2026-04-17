"""
One-Time Pad Cipher — Optimized Variants & Benchmark
======================================================
Three implementations of the pseudo-random OTP encryption.
"""

import random
import timeit


# Variant 1: Original loop-based approach
def encrypt_v1(text: str) -> tuple[list[int], list[int]]:
    plain = [ord(c) for c in text]
    keys = [random.randint(1, 300) for _ in plain]
    cipher = [(p + k) * k for p, k in zip(plain, keys)]
    return cipher, keys


# Variant 2: Single-pass list comprehension
def encrypt_v2(text: str) -> tuple[list[int], list[int]]:
    keys = [random.randint(1, 300) for _ in text]
    cipher = [(ord(c) + k) * k for c, k in zip(text, keys)]
    return cipher, keys


# Variant 3: Functional style with map
def encrypt_v3(text: str) -> tuple[list[int], list[int]]:
    keys = list(map(lambda _: random.randint(1, 300), text))
    cipher = list(map(lambda ck: (ord(ck[0]) + ck[1]) * ck[1], zip(text, keys)))
    return cipher, keys


def decrypt_v1(cipher: list[int], key: list[int]) -> str:
    return "".join(chr(int((c - k**2) / k)) for c, k in zip(cipher, key))


def benchmark(n: int = 100_000) -> None:
    setup = (
        "import random; random.seed(42); "
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "msg = 'Hello World'"
    )
    t1 = timeit.timeit("encrypt_v1(msg)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(msg)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(msg)", setup=setup, number=n)
    print(f"V1 (zip loop)   : {t1:.4f}s for {n:,} runs")
    print(f"V2 (listcomp)   : {t2:.4f}s for {n:,} runs")
    print(f"V3 (map)        : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    random.seed(1)
    cipher, key = encrypt_v1("Hello")
    print("Cipher:", cipher)
    print("Keys  :", key)
    print("Decrypted:", decrypt_v1(cipher, key))
    benchmark()
