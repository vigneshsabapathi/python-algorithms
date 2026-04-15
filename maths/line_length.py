"""
Line length by numerical integration of arc length:
    L = ∫_a^b sqrt(1 + (f'(x))^2) dx

We approximate with the trapezoidal rule on piecewise-linear segments.

>>> round(line_length(lambda x: x, 0, 10), 6)
14.142136
>>> round(line_length(lambda x: 2*x + 1, 0, 5), 6)
11.18034
"""

import math


def line_length(fn, a: float, b: float, steps: int = 1000) -> float:
    """Approximate arc length of y = fn(x) on [a, b].

    >>> round(line_length(lambda x: x*x, 0, 1, 10000), 3)
    1.479
    """
    if a >= b:
        raise ValueError("a must be less than b")
    h = (b - a) / steps
    total = 0.0
    prev_x, prev_y = a, fn(a)
    for i in range(1, steps + 1):
        x = a + i * h
        y = fn(x)
        total += math.hypot(x - prev_x, y - prev_y)
        prev_x, prev_y = x, y
    return total


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(round(line_length(lambda x: x, 0, 10), 6))
