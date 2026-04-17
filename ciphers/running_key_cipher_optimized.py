"""
Running Key Cipher — Optimized Variants & Benchmark
=====================================================
"""

import timeit


# Variant 1: Original generator expression
def encrypt_v1(key: str, plaintext: str) -> str:
    pt = plaintext.replace(" ", "").upper()
    k = key.replace(" ", "").upper()
    kl = len(k)
    ord_a = ord("A")
    return "".join(
        chr(((ord(c) - ord_a + ord(k[i % kl]) - ord_a) % 26) + ord_a)
        for i, c in enumerate(pt)
    )


# Variant 2: Precomputed key ordinals
def encrypt_v2(key: str, plaintext: str) -> str:
    pt = plaintext.replace(" ", "").upper()
    k = key.replace(" ", "").upper()
    key_ords = [ord(c) - 65 for c in k]
    kl = len(key_ords)
    return "".join(
        chr(((ord(c) - 65 + key_ords[i % kl]) % 26) + 65)
        for i, c in enumerate(pt)
    )


# Variant 3: Bytes-level arithmetic
def encrypt_v3(key: str, plaintext: str) -> str:
    pt = plaintext.replace(" ", "").upper()
    k = key.replace(" ", "").upper()
    key_ords = [ord(c) - 65 for c in k]
    kl = len(key_ords)
    result = bytearray(len(pt))
    for i, c in enumerate(pt):
        result[i] = ((ord(c) - 65 + key_ords[i % kl]) % 26) + 65
    return result.decode("ascii")


def benchmark(n: int = 100_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "key = 'How does the duck know that? said Victor'; "
        "msg = 'DEFEND THE EAST WALL OF THE CASTLE'"
    )
    t1 = timeit.timeit("encrypt_v1(key, msg)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(key, msg)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(key, msg)", setup=setup, number=n)
    print(f"V1 (genexpr)     : {t1:.4f}s for {n:,} runs")
    print(f"V2 (precomp ord) : {t2:.4f}s for {n:,} runs")
    print(f"V3 (bytearray)   : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    key = "How does the duck know that? said Victor"
    msg = "DEFEND THIS"
    print("V1:", encrypt_v1(key, msg))
    print("V2:", encrypt_v2(key, msg))
    print("V3:", encrypt_v3(key, msg))
    benchmark()
