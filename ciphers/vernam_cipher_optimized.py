"""
Vernam Cipher — Optimized Variants & Benchmark
================================================
Three implementations of the repeating-key XOR-on-alphabet cipher.
"""

import timeit


# Variant 1: Original character-by-character loop
def encrypt_v1(plaintext: str, key: str) -> str:
    ct = ""
    for i, ch in enumerate(plaintext):
        ct += chr(65 + (ord(ch) - 65 + ord(key[i % len(key)]) - 65) % 26)
    return ct


# Variant 2: List comprehension (avoids string concatenation overhead)
def encrypt_v2(plaintext: str, key: str) -> str:
    klen = len(key)
    return "".join(
        chr(65 + (ord(ch) - 65 + ord(key[i % klen]) - 65) % 26)
        for i, ch in enumerate(plaintext)
    )


# Variant 3: Precomputed key ordinals
def encrypt_v3(plaintext: str, key: str) -> str:
    key_ords = [ord(k) - 65 for k in key]
    klen = len(key_ords)
    return "".join(
        chr(65 + (ord(ch) - 65 + key_ords[i % klen]) % 26)
        for i, ch in enumerate(plaintext)
    )


def decrypt_v1(ciphertext: str, key: str) -> str:
    return "".join(
        chr(65 + (ord(ch) - ord(key[i % len(key)])) % 26)
        for i, ch in enumerate(ciphertext)
    )


def benchmark(n: int = 200_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "pt = 'HELLOWORLD'; key = 'KEY'"
    )
    t1 = timeit.timeit("encrypt_v1(pt, key)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(pt, key)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(pt, key)", setup=setup, number=n)
    print(f"V1 (concat loop) : {t1:.4f}s for {n:,} runs")
    print(f"V2 (genexpr)     : {t2:.4f}s for {n:,} runs")
    print(f"V3 (precomp ord) : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    pt, key = "HELLO", "KEY"
    enc = encrypt_v1(pt, key)
    print("V1 encrypted:", enc)
    print("V2 encrypted:", encrypt_v2(pt, key))
    print("V3 encrypted:", encrypt_v3(pt, key))
    print("Decrypted   :", decrypt_v1(enc, key))
    print()
    benchmark()
