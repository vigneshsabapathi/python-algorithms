"""
Sumset variants + benchmark.

1. setcomp        - {a+b for a in A for b in B}
2. nested_loop    - explicit double loop, set add
3. fft_indicator  - polynomial multiplication via FFT (for integer sets)
"""
from __future__ import annotations

import time
from typing import Iterable


def setcomp(A, B):
    return {a + b for a in A for b in B}


def nested_loop(A, B):
    out = set()
    for a in A:
        for b in B:
            out.add(a + b)
    return out


def fft_indicator(A, B):
    """For non-negative integer sets, A+B equals the support of P_A * P_B."""
    if not A or not B:
        return set()
    M = max(max(A), max(B))
    pa = [0] * (M + 1)
    pb = [0] * (M + 1)
    for x in A:
        pa[x] = 1
    for x in B:
        pb[x] = 1
    n = 1
    while n < 2 * (M + 1):
        n <<= 1
    # naive convolution (FFT would be better; staying pure-py for safety)
    conv = [0] * (2 * M + 1)
    for i, ai in enumerate(pa):
        if ai:
            for j, bj in enumerate(pb):
                if bj:
                    conv[i + j] = 1
    return {i for i, v in enumerate(conv) if v}


def benchmark() -> None:
    A = set(range(0, 200))
    B = set(range(0, 200))
    print(f"{'fn':<16}{'|A+B|':>10}{'ms':>12}")
    for fn in (setcomp, nested_loop, fft_indicator):
        t = time.perf_counter()
        s = fn(A, B)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<16}{len(s):>10}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
