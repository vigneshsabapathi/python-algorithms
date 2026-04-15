"""
Rectangular to Polar - Optimized Variants with Benchmarks
"""

import timeit
import math
import cmath


def rect_to_polar_math(x: float, y: float) -> tuple[float, float]:
    """
    Standard math.sqrt + math.atan2.

    >>> rect_to_polar_math(3, 4)
    (5.0, 0.9273)
    """
    return round(math.sqrt(x*x + y*y), 5), round(math.atan2(y, x), 4)


def rect_to_polar_hypot(x: float, y: float) -> tuple[float, float]:
    """
    math.hypot (optimized C implementation for magnitude).

    >>> rect_to_polar_hypot(3, 4)
    (5.0, 0.9273)
    """
    return round(math.hypot(x, y), 5), round(math.atan2(y, x), 4)


def rect_to_polar_cmath(x: float, y: float) -> tuple[float, float]:
    """
    cmath.polar using complex numbers.

    >>> rect_to_polar_cmath(3, 4)
    (5.0, 0.9273)
    """
    r, theta = cmath.polar(complex(x, y))
    return round(r, 5), round(theta, 4)


def benchmark():
    number = 200_000
    print(f"Benchmark: (3, 4) -> polar ({number:,} iterations)\n")
    results = []
    for label, func in [("math.sqrt+atan2", rect_to_polar_math),
                         ("math.hypot", rect_to_polar_hypot),
                         ("cmath.polar", rect_to_polar_cmath)]:
        t = timeit.timeit(lambda: func(3, 4), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
