"""Odd sieve — variants + benchmark."""

import time


def sieve_basic(n):
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]


def sieve_odd(n):
    if n < 2:
        return []
    if n == 2:
        return [2]
    size = (n - 1) // 2
    sieve = [True] * size
    i = 0
    while (2 * i + 3) ** 2 <= n:
        if sieve[i]:
            p = 2 * i + 3
            start = (p * p - 3) // 2
            for j in range(start, size, p):
                sieve[j] = False
        i += 1
    return [2] + [2 * i + 3 for i in range(size) if sieve[i]]


def sieve_odd_slice(n):
    """Use slice assignment for faster marking."""
    if n < 2:
        return []
    if n == 2:
        return [2]
    size = (n - 1) // 2
    sieve = bytearray([1]) * size
    i = 0
    while (2 * i + 3) ** 2 <= n:
        if sieve[i]:
            p = 2 * i + 3
            start = (p * p - 3) // 2
            sieve[start::p] = bytearray(len(sieve[start::p]))
        i += 1
    return [2] + [2 * i + 3 for i in range(size) if sieve[i]]


def benchmark():
    N = 2_000_000
    for name, fn in [
        ("basic_sieve", sieve_basic),
        ("odd_only_list", sieve_odd),
        ("odd_bytearray_slice", sieve_odd_slice),
    ]:
        start = time.perf_counter()
        r = fn(N)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:22s} count={len(r)}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
