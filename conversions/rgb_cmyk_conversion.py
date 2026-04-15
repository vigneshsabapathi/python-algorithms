"""
RGB to CMYK Conversion

Convert between RGB and CMYK color spaces.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/rgb_cmyk_conversion.py
"""


def rgb_to_cmyk(
    red: int, green: int, blue: int
) -> tuple[float, float, float, float]:
    """
    Convert RGB (0-255) to CMYK (0-1 each).

    >>> rgb_to_cmyk(255, 0, 0)
    (0.0, 1.0, 1.0, 0.0)
    >>> rgb_to_cmyk(0, 255, 0)
    (1.0, 0.0, 1.0, 0.0)
    >>> rgb_to_cmyk(0, 0, 255)
    (1.0, 1.0, 0.0, 0.0)
    >>> rgb_to_cmyk(255, 255, 255)
    (0.0, 0.0, 0.0, 0.0)
    >>> rgb_to_cmyk(0, 0, 0)
    (0.0, 0.0, 0.0, 1.0)
    """
    if not all(0 <= c <= 255 for c in (red, green, blue)):
        raise ValueError("RGB values must be between 0 and 255")

    r, g, b = red / 255.0, green / 255.0, blue / 255.0

    k = 1.0 - max(r, g, b)
    if k == 1.0:
        return (0.0, 0.0, 0.0, 1.0)

    c = round((1.0 - r - k) / (1.0 - k), 5)
    m = round((1.0 - g - k) / (1.0 - k), 5)
    y = round((1.0 - b - k) / (1.0 - k), 5)
    k = round(k, 5)

    return (c, m, y, k)


def cmyk_to_rgb(
    cyan: float, magenta: float, yellow: float, key: float
) -> tuple[int, int, int]:
    """
    Convert CMYK (0-1 each) to RGB (0-255).

    >>> cmyk_to_rgb(0, 1, 1, 0)
    (255, 0, 0)
    >>> cmyk_to_rgb(1, 0, 1, 0)
    (0, 255, 0)
    >>> cmyk_to_rgb(1, 1, 0, 0)
    (0, 0, 255)
    >>> cmyk_to_rgb(0, 0, 0, 0)
    (255, 255, 255)
    >>> cmyk_to_rgb(0, 0, 0, 1)
    (0, 0, 0)
    """
    if not all(0 <= v <= 1 for v in (cyan, magenta, yellow, key)):
        raise ValueError("CMYK values must be between 0 and 1")

    r = round(255 * (1 - cyan) * (1 - key))
    g = round(255 * (1 - magenta) * (1 - key))
    b = round(255 * (1 - yellow) * (1 - key))

    return (r, g, b)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 0), (255, 255, 255)]
    for r, g, b in colors:
        c, m, y, k = rgb_to_cmyk(r, g, b)
        back = cmyk_to_rgb(c, m, y, k)
        print(f"  RGB({r},{g},{b}) -> CMYK({c},{m},{y},{k}) -> RGB{back}")
