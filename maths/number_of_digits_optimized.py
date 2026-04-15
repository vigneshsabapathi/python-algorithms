"""Number of digits — variants + benchmark."""

import math
import time
import random


def digits_log(n):
    if n == 0:
        return 1
    return int(math.log10(abs(n))) + 1


def digits_str(n):
    return len(str(abs(n)))


def digits_loop(n):
    n = abs(n)
    if n == 0:
        return 1
    c = 0
    while n:
        n //= 10
        c += 1
    return c


def benchmark():
    small = [random.randint(0, 10**9) for _ in range(100_000)]
    big = [random.randint(10**100, 10**200) for _ in range(1000)]
    for name, fn in [("log10_cast", digits_log), ("str_len", digits_str), ("div10_loop", digits_loop)]:
        start = time.perf_counter()
        for v in small:
            fn(v)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:15s} small  time={elapsed:.3f} ms")
    for name, fn in [("str_len", digits_str), ("div10_loop", digits_loop)]:
        start = time.perf_counter()
        for v in big:
            fn(v)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:15s} big    time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
