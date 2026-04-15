"""Line length — variants + benchmark."""

import math
import time


def line_piecewise(fn, a, b, steps=1000):
    h = (b - a) / steps
    total = 0.0
    px, py = a, fn(a)
    for i in range(1, steps + 1):
        x = a + i * h
        y = fn(x)
        total += math.hypot(x - px, y - py)
        px, py = x, y
    return total


def line_trapezoidal_ds(fn, a, b, steps=1000, dx=1e-6):
    """∫ sqrt(1 + (f')²) dx with numerical derivative."""
    h = (b - a) / steps
    total = 0.0
    for i in range(steps):
        x = a + i * h
        deriv = (fn(x + dx) - fn(x - dx)) / (2 * dx)
        total += math.sqrt(1 + deriv * deriv) * h
    return total


def line_simpson(fn, a, b, steps=1000, dx=1e-6):
    """Simpson's rule for arc length integral."""
    if steps % 2:
        steps += 1
    h = (b - a) / steps

    def g(x):
        d = (fn(x + dx) - fn(x - dx)) / (2 * dx)
        return math.sqrt(1 + d * d)

    total = g(a) + g(b)
    for i in range(1, steps):
        x = a + i * h
        total += (4 if i % 2 else 2) * g(x)
    return total * h / 3


def benchmark():
    f = lambda x: x * x
    for name, fn in [
        ("piecewise_hypot", lambda: line_piecewise(f, 0, 1, 10_000)),
        ("trap_numeric_d", lambda: line_trapezoidal_ds(f, 0, 1, 10_000)),
        ("simpson", lambda: line_simpson(f, 0, 1, 10_000)),
    ]:
        start = time.perf_counter()
        r = fn()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:18s} len={r:.6f}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
