"""
RGB CMYK Conversion - Optimized Variants with Benchmarks
"""

import timeit


def rgb_to_cmyk_standard(r: int, g: int, b: int) -> tuple[float, float, float, float]:
    """
    Standard formula.

    >>> rgb_to_cmyk_standard(255, 0, 0)
    (0.0, 1.0, 1.0, 0.0)
    """
    r, g, b = r / 255, g / 255, b / 255
    k = 1 - max(r, g, b)
    if k == 1:
        return (0.0, 0.0, 0.0, 1.0)
    d = 1 - k
    return round((1 - r - k) / d, 5), round((1 - g - k) / d, 5), round((1 - b - k) / d, 5), round(k, 5)


def rgb_to_cmyk_inlined(r: int, g: int, b: int) -> tuple[float, float, float, float]:
    """
    Inlined operations, fewer divisions.

    >>> rgb_to_cmyk_inlined(255, 0, 0)
    (0.0, 1.0, 1.0, 0.0)
    """
    rf, gf, bf = r * 0.003921568627451, g * 0.003921568627451, b * 0.003921568627451
    mx = max(rf, gf, bf)
    if mx == 0:
        return (0.0, 0.0, 0.0, 1.0)
    inv = 1.0 / mx
    return round(1 - rf * inv, 5), round(1 - gf * inv, 5), round(1 - bf * inv, 5), round(1 - mx, 5) + 0.0


def rgb_to_cmyk_bitwise(r: int, g: int, b: int) -> tuple[float, float, float, float]:
    """
    Integer math where possible before float conversion.

    >>> rgb_to_cmyk_bitwise(255, 0, 0)
    (0.0, 1.0, 1.0, 0.0)
    """
    mx = max(r, g, b)
    if mx == 0:
        return (0.0, 0.0, 0.0, 1.0)
    inv = 1.0 / mx
    return round(1 - r * inv, 5), round(1 - g * inv, 5), round(1 - b * inv, 5), round(1 - mx / 255, 5)


def benchmark():
    number = 200_000
    print(f"Benchmark: RGB(128,64,200) -> CMYK ({number:,} iterations)\n")
    results = []
    for label, func in [("Standard", rgb_to_cmyk_standard),
                         ("Inlined", rgb_to_cmyk_inlined),
                         ("Bitwise/int", rgb_to_cmyk_bitwise)]:
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
