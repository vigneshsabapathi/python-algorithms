"""
sin(x) variants + benchmark.

1. math_sin     - math.sin (C / libm)
2. taylor       - Maclaurin series with argument reduction
3. cordic       - CORDIC iteration (no division/multiplication in classic form)
"""
from __future__ import annotations

import math
import time


def math_sin(x: float) -> float:
    return math.sin(x)


def taylor(x: float, terms: int = 20) -> float:
    x = ((x + math.pi) % (2 * math.pi)) - math.pi
    s, term = 0.0, x
    for k in range(terms):
        s += term
        term *= -(x * x) / ((2 * k + 2) * (2 * k + 3))
    return s


_CORDIC_K = 0.6072529350088812561694
_CORDIC_ANGLES = [math.atan(2 ** -i) for i in range(30)]


def cordic(x: float) -> float:
    # reduce to [-pi/2, pi/2]
    x = ((x + math.pi) % (2 * math.pi)) - math.pi
    negate = False
    if x > math.pi / 2:
        x = math.pi - x
    elif x < -math.pi / 2:
        x = -math.pi - x
        negate = True
    # cordic rotation: start (1, 0), target angle x
    u, v, theta = 1.0, 0.0, 0.0
    for i, ang in enumerate(_CORDIC_ANGLES):
        if theta < x:
            u, v = u - v * (2 ** -i), v + u * (2 ** -i)
            theta += ang
        else:
            u, v = u + v * (2 ** -i), v - u * (2 ** -i)
            theta -= ang
    result = v * _CORDIC_K
    return -result if negate else result


def benchmark() -> None:
    xs = [0, math.pi / 6, math.pi / 2, math.pi, 10.0]
    print(f"{'fn':<12}{'x':>12}{'sin(x)':>14}{'ms':>10}")
    for fn in (math_sin, taylor, cordic):
        for x in xs:
            t = time.perf_counter()
            for _ in range(10000):
                r = fn(x)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<12}{x:>12.4f}{r:>14.6f}{dt:>10.3f}")


if __name__ == "__main__":
    benchmark()
