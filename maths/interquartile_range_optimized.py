"""IQR — variants + benchmark."""

import time
import random
import statistics


def iqr_manual(data):
    s = sorted(data)
    n = len(s)

    def q(p):
        pos = (n - 1) * p
        lo = int(pos)
        hi = min(lo + 1, n - 1)
        return s[lo] * (1 - (pos - lo)) + s[hi] * (pos - lo)

    return q(0.75) - q(0.25)


def iqr_statistics(data):
    q = statistics.quantiles(data, n=4, method="inclusive")
    return q[2] - q[0]


def iqr_numpy(data):
    try:
        import numpy as np  # type: ignore
    except ImportError:
        return iqr_manual(data)
    return float(np.percentile(data, 75) - np.percentile(data, 25))


def benchmark():
    data = [random.gauss(0, 1) for _ in range(100_000)]
    for name, fn in [
        ("manual_interp", iqr_manual),
        ("statistics.quantiles", iqr_statistics),
        ("numpy.percentile", iqr_numpy),
    ]:
        start = time.perf_counter()
        r = fn(data)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:22s} iqr={r:.4f}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
