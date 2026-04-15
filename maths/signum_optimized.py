"""
Signum variants + benchmark.

1. branched       - explicit if/else
2. compare        - (x > 0) - (x < 0)
3. math_copysign  - math.copysign(1, x), but returns +1 for x=0
4. numpy_sign     - numpy.sign
"""
from __future__ import annotations

import math
import time


def branched(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


def compare(x):
    return (x > 0) - (x < 0)


def math_copysign(x):
    if x == 0:
        return 0
    return int(math.copysign(1, x))


def numpy_sign(x):
    try:
        import numpy as np
    except ImportError:
        return branched(x)
    return int(np.sign(x))


def benchmark() -> None:
    xs = [-3, 0, 0.5, 7.7]
    print(f"{'fn':<16}{'ms':>12}")
    for fn in (branched, compare, math_copysign, numpy_sign):
        t = time.perf_counter()
        for _ in range(1_000_000):
            for x in xs:
                fn(x)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<16}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
