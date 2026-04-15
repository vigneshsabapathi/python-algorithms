"""Juggler sequence — variants + benchmark."""

import math
import time


def juggler_isqrt(n):
    seq = [n]
    while n != 1:
        if n % 2 == 0:
            n = math.isqrt(n)
        else:
            n = math.isqrt(n * n * n)
        seq.append(n)
    return seq


def juggler_float(n):
    """Uses float — fast but loses precision for large n."""
    seq = [n]
    while n != 1:
        if n % 2 == 0:
            n = int(n**0.5)
        else:
            n = int(n**1.5)
        seq.append(n)
    return seq


def juggler_length_only(n):
    """Don't build list — just count."""
    k = 0
    while n != 1:
        n = math.isqrt(n) if n % 2 == 0 else math.isqrt(n * n * n)
        k += 1
    return k


def benchmark():
    starts = list(range(2, 1000))
    for name, fn in [
        ("isqrt_full_seq", lambda: [juggler_isqrt(s) for s in starts]),
        ("float_full_seq", lambda: [juggler_float(s) for s in starts]),
        ("length_only", lambda: [juggler_length_only(s) for s in starts]),
    ]:
        start = time.perf_counter()
        fn()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:18s} time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
