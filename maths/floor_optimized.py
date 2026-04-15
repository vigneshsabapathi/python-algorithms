"""Floor — variants + benchmark."""

import math
import time
import random


def floor_cast(x):
    i = int(x)
    return i if x >= 0 or x == i else i - 1


def floor_math(x):
    return math.floor(x)


def floor_bitshift(x):
    # Only exact for integer-valued floats via int cast trick
    if x >= 0:
        return int(x)
    return -(int(-x) + (1 if -x != int(-x) else 0))


def benchmark():
    data = [random.uniform(-1e6, 1e6) for _ in range(200_000)]
    for name, fn in [
        ("int_cast", floor_cast),
        ("math.floor", floor_math),
        ("neg_trick", floor_bitshift),
    ]:
        start = time.perf_counter()
        for v in data:
            fn(v)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:15s} time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
