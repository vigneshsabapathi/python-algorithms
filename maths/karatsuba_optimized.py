"""Karatsuba — variants + benchmark."""

import time
import random


def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    power = 10**m
    hx, lx = divmod(x, power)
    hy, ly = divmod(y, power)
    z0 = karatsuba(lx, ly)
    z2 = karatsuba(hx, hy)
    z1 = karatsuba(lx + hx, ly + hy) - z0 - z2
    return z2 * 10 ** (2 * m) + z1 * 10**m + z0


def karatsuba_bit_split(x, y):
    """Split using bit halves (faster base-2 shifting)."""
    if x < 1024 or y < 1024:
        return x * y
    n = max(x.bit_length(), y.bit_length())
    m = n // 2
    mask = (1 << m) - 1
    lx = x & mask
    hx = x >> m
    ly = y & mask
    hy = y >> m
    z0 = karatsuba_bit_split(lx, ly)
    z2 = karatsuba_bit_split(hx, hy)
    z1 = karatsuba_bit_split(lx + hx, ly + hy) - z0 - z2
    return (z2 << (2 * m)) + (z1 << m) + z0


def schoolbook(x, y):
    return x * y  # Python built-in (uses Karatsuba internally for big ints)


def benchmark():
    # 1000-digit numbers
    a = random.randint(10**999, 10**1000)
    b = random.randint(10**999, 10**1000)
    for name, fn in [
        ("karatsuba_decimal", karatsuba),
        ("karatsuba_bitsplit", karatsuba_bit_split),
        ("python_builtin", schoolbook),
    ]:
        start = time.perf_counter()
        r = fn(a, b)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:22s} digits={len(str(r))}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
