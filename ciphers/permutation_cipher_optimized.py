"""
Permutation Cipher — Optimized Variants & Benchmark
=====================================================
Three implementations of block-level permutation encryption.
"""

import timeit


# Variant 1: Original join-index approach
def encrypt_v1(message: str, key: list[int], block_size: int) -> str:
    message = message.upper()
    enc = ""
    for i in range(0, len(message), block_size):
        block = message[i : i + block_size]
        enc += "".join(block[j] for j in key if j < len(block))
    return enc


# Variant 2: Pre-allocate list
def encrypt_v2(message: str, key: list[int], block_size: int) -> str:
    message = message.upper()
    parts: list[str] = []
    for i in range(0, len(message), block_size):
        block = message[i : i + block_size]
        parts.append("".join(block[j] for j in key if j < len(block)))
    return "".join(parts)


# Variant 3: NumPy-style index trick with zip
def encrypt_v3(message: str, key: list[int], block_size: int) -> str:
    message = message.upper()
    padded = message.ljust((len(message) + block_size - 1) // block_size * block_size)
    blocks = [padded[i : i + block_size] for i in range(0, len(padded), block_size)]
    return "".join(
        "".join(b[j] for j in key)
        for b in blocks
    )[: len(message)]


def benchmark(n: int = 100_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "msg = 'HELLOWORLD' * 5; key = [1,0,3,2]; bs = 4"
    )
    t1 = timeit.timeit("encrypt_v1(msg, key, bs)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(msg, key, bs)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(msg, key, bs)", setup=setup, number=n)
    print(f"V1 (concat)    : {t1:.4f}s for {n:,} runs")
    print(f"V2 (list parts): {t2:.4f}s for {n:,} runs")
    print(f"V3 (padded)    : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    msg = "HELLOWORLD"
    key = [1, 0, 3, 2]
    bs = 4
    print("V1:", encrypt_v1(msg, key, bs))
    print("V2:", encrypt_v2(msg, key, bs))
    print("V3:", encrypt_v3(msg, key, bs))
    benchmark()
