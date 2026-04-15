"""Fermat's Little Theorem — variants & benchmark."""

import time


def flt_naive(a: int, p: int) -> int:
    """O(p) multiplication loop."""
    result = 1
    for _ in range(p - 1):
        result = (result * a) % p
    return result


def flt_fast_pow(a: int, p: int) -> int:
    """O(log p) via built-in pow."""
    return pow(a, p - 1, p)


def flt_manual_binpow(a: int, p: int) -> int:
    """Manual binary exponentiation."""
    exp = p - 1
    result = 1
    a %= p
    while exp > 0:
        if exp & 1:
            result = (result * a) % p
        a = (a * a) % p
        exp >>= 1
    return result


def benchmark():
    a, p = 7, 1_000_003  # prime
    for name, fn in [
        ("naive", flt_naive),
        ("fast_pow", flt_fast_pow),
        ("manual_binpow", flt_manual_binpow),
    ]:
        start = time.perf_counter()
        r = fn(a, p)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} result={r}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
