"""Matrix exponentiation — variants + benchmark."""

import time


def mat_mul(a, b):
    n, m, k = len(a), len(b[0]), len(b)
    r = [[0] * m for _ in range(n)]
    for i in range(n):
        row = r[i]
        a_i = a[i]
        for p in range(k):
            v = a_i[p]
            if v == 0:
                continue
            b_p = b[p]
            for j in range(m):
                row[j] += v * b_p[j]
    return r


def mat_pow_iter(M, p):
    n = len(M)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = [row[:] for row in M]
    while p:
        if p & 1:
            result = mat_mul(result, base)
        base = mat_mul(base, base)
        p >>= 1
    return result


def mat_pow_recursive(M, p):
    if p == 0:
        n = len(M)
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    if p == 1:
        return M
    half = mat_pow_recursive(M, p // 2)
    sq = mat_mul(half, half)
    return mat_mul(sq, M) if p & 1 else sq


def mat_pow_2x2_unrolled(a, b, c, d, p):
    """Specialized 2x2 matrix power — returns (a, b, c, d)."""
    ra, rb, rc, rd = 1, 0, 0, 1
    while p:
        if p & 1:
            ra, rb, rc, rd = (
                ra * a + rb * c,
                ra * b + rb * d,
                rc * a + rd * c,
                rc * b + rd * d,
            )
        a, b, c, d = a * a + b * c, a * b + b * d, c * a + d * c, c * b + d * d
        p >>= 1
    return ra, rb, rc, rd


def benchmark():
    M = [[1, 1], [1, 0]]
    p = 10_000
    for name, fn in [
        ("iterative_generic", lambda: mat_pow_iter(M, p)),
        ("recursive_generic", lambda: mat_pow_recursive(M, p)),
        ("unrolled_2x2", lambda: mat_pow_2x2_unrolled(1, 1, 1, 0, p)),
    ]:
        start = time.perf_counter()
        fn()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:22s} time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
