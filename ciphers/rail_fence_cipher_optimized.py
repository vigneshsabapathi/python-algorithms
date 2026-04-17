"""
Rail Fence Cipher — Optimized Variants & Benchmark
====================================================
Three implementations of the rail fence encryption.
"""

import timeit


# Variant 1: Original list-of-lists approach
def encrypt_v1(message: str, key: int) -> str:
    if key <= 0:
        raise ValueError("key must be positive")
    if key == 1 or len(message) <= key:
        return message
    grid: list[list[str]] = [[] for _ in range(key)]
    low = key - 1
    for pos, c in enumerate(message):
        n = pos % (low * 2)
        n = min(n, low * 2 - n)
        grid[n].append(c)
    return "".join("".join(row) for row in grid)


# Variant 2: Direct index computation, no nested lists
def encrypt_v2(message: str, key: int) -> str:
    if key <= 0:
        raise ValueError("key must be positive")
    if key == 1 or len(message) <= key:
        return message
    rails: list[list[str]] = [[] for _ in range(key)]
    cycle = 2 * (key - 1)
    for i, c in enumerate(message):
        r = i % cycle
        rails[min(r, cycle - r)].append(c)
    return "".join("".join(rail) for rail in rails)


# Variant 3: sorted-index approach (no mutation, functional style)
def encrypt_v3(message: str, key: int) -> str:
    if key <= 0:
        raise ValueError("key must be positive")
    if key == 1 or len(message) <= key:
        return message
    cycle = 2 * (key - 1)
    indices = sorted(
        range(len(message)),
        key=lambda i: (min(i % cycle, cycle - i % cycle), i),
    )
    return "".join(message[i] for i in indices)


def benchmark(n: int = 50_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "msg = 'WEAREDISCOVEREDRUNATONCE' * 5; key = 3"
    )
    t1 = timeit.timeit("encrypt_v1(msg, key)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(msg, key)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(msg, key)", setup=setup, number=n)
    print(f"V1 (original)  : {t1:.4f}s for {n:,} runs")
    print(f"V2 (cycle)     : {t2:.4f}s for {n:,} runs")
    print(f"V3 (sorted idx): {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    msg = "WEAREDISCOVEREDRUNATONCE"
    enc = encrypt_v1(msg, 3)
    print("Encrypted:", enc)
    print()
    benchmark()
