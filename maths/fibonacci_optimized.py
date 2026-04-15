"""Fibonacci — 4 variants + benchmark."""

import time
from functools import lru_cache


def fib_iter(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


def fib_matrix(n: int) -> int:
    """O(log n) via fast matrix exponentiation."""

    def mul(A, B):
        return (
            A[0] * B[0] + A[1] * B[2],
            A[0] * B[1] + A[1] * B[3],
            A[2] * B[0] + A[3] * B[2],
            A[2] * B[1] + A[3] * B[3],
        )

    def mpow(M, p):
        result = (1, 0, 0, 1)
        while p:
            if p & 1:
                result = mul(result, M)
            M = mul(M, M)
            p >>= 1
        return result

    if n == 0:
        return 0
    return mpow((1, 1, 1, 0), n)[1]


def fib_doubling(n: int) -> int:
    """Fast doubling O(log n)."""

    def helper(k):
        if k == 0:
            return (0, 1)
        a, b = helper(k >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        if k & 1:
            return (d, c + d)
        return (c, d)

    return helper(n)[0]


def benchmark():
    n = 10_000
    fib_memo.cache_clear()
    for name, fn in [
        ("iterative", fib_iter),
        ("matrix_pow", fib_matrix),
        ("fast_doubling", fib_doubling),
    ]:
        start = time.perf_counter()
        r = fn(n)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} digits={len(str(r))}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
