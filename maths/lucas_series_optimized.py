"""Lucas numbers — variants + benchmark."""

import time


def lucas_iter(n):
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def lucas_formula(n):
    """L(n) = F(n-1) + F(n+1) using fast doubling."""

    def fib_pair(k):
        if k == 0:
            return (0, 1)
        a, b = fib_pair(k >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        if k & 1:
            return (d, c + d)
        return (c, d)

    if n == 0:
        return 2
    f_prev, f_cur = fib_pair(n - 1) if n >= 1 else (0, 1)
    return f_prev + f_cur + (f_prev)  # L(n) = F(n-1) + F(n+1) = F(n-1) + F(n) + F(n-1)? use identity directly
    # correct: L(n) = 2*F(n+1) - F(n)


def lucas_identity(n):
    """L(n) = 2*F(n+1) - F(n) using fast doubling of F."""

    def fib(k):
        def helper(m):
            if m == 0:
                return (0, 1)
            a, b = helper(m >> 1)
            c = a * (2 * b - a)
            d = a * a + b * b
            if m & 1:
                return (d, c + d)
            return (c, d)

        return helper(k)[0]

    return 2 * fib(n + 1) - fib(n)


def lucas_doubling(n):
    """Fast doubling using Fibonacci identity L(n) = F(n-1) + F(n+1),
    computed via a single fast-doubling pass."""

    def fib_pair(k):
        # returns (F(k), F(k+1))
        if k == 0:
            return (0, 1)
        a, b = fib_pair(k >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        if k & 1:
            return (d, c + d)
        return (c, d)

    if n == 0:
        return 2
    if n == 1:
        return 1
    # F(n-1) + F(n+1) = F(n-1) + F(n) + F(n-1) -- nope. Use: F(n-1)+F(n+1)
    f_n, f_np1 = fib_pair(n)
    f_nm1 = f_np1 - f_n
    return f_nm1 + f_np1


def benchmark():
    n = 5000
    for name, fn in [
        ("iterative", lucas_iter),
        ("fib_identity", lucas_identity),
        ("direct_doubling", lucas_doubling),
    ]:
        start = time.perf_counter()
        r = fn(n)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} digits={len(str(r))}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
