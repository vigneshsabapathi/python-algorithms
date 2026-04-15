"""
RGB HSV Conversion - Optimized Variants with Benchmarks
"""

import timeit
import colorsys


def rgb_to_hsv_manual(r: int, g: int, b: int) -> tuple[float, float, float]:
    """
    Manual formula implementation.

    >>> rgb_to_hsv_manual(255, 0, 0)
    (0.0, 1.0, 1.0)
    """
    r, g, b = r / 255, g / 255, b / 255
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d == 0: h = 0.0
    elif mx == r: h = 60 * (((g - b) / d) % 6)
    elif mx == g: h = 60 * (((b - r) / d) + 2)
    else: h = 60 * (((r - g) / d) + 4)
    s = 0.0 if mx == 0 else d / mx
    return round(h, 5), round(s, 5), round(mx, 5)


def rgb_to_hsv_colorsys(r: int, g: int, b: int) -> tuple[float, float, float]:
    """
    Python colorsys library (returns H in 0-1, scaled to 0-360).

    >>> rgb_to_hsv_colorsys(255, 0, 0)
    (0.0, 1.0, 1.0)
    """
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return round(h * 360, 5), round(s, 5), round(v, 5)


def rgb_to_hsv_optimized(r: int, g: int, b: int) -> tuple[float, float, float]:
    """
    Inlined with minimal branching.

    >>> rgb_to_hsv_optimized(255, 0, 0)
    (0.0, 1.0, 1.0)
    """
    r, g, b = r * 0.003921568627451, g * 0.003921568627451, b * 0.003921568627451  # /255
    mx = r if r > g else g
    if b > mx: mx = b
    mn = r if r < g else g
    if b < mn: mn = b
    d = mx - mn
    if d == 0: h = 0.0
    elif mx == r: h = 60 * (((g - b) / d) % 6)
    elif mx == g: h = 60 * ((b - r) / d + 2)
    else: h = 60 * ((r - g) / d + 4)
    s = 0 if mx == 0 else d / mx
    return round(h, 5), round(s, 5), round(mx, 5)


def benchmark():
    number = 200_000
    print(f"Benchmark: RGB(128,64,200) -> HSV ({number:,} iterations)\n")
    results = []
    for label, func in [("Manual", rgb_to_hsv_manual),
                         ("colorsys", rgb_to_hsv_colorsys),
                         ("Optimized", rgb_to_hsv_optimized)]:
        t = timeit.timeit(lambda: func(128, 64, 200), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
