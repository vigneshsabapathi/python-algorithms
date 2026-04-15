"""
RGB to HSV Conversion

Convert between RGB and HSV color spaces.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/rgb_hsv_conversion.py
"""


def rgb_to_hsv(red: int, green: int, blue: int) -> tuple[float, float, float]:
    """
    Convert RGB (0-255) to HSV (H: 0-360, S: 0-1, V: 0-1).

    >>> rgb_to_hsv(255, 0, 0)
    (0.0, 1.0, 1.0)
    >>> rgb_to_hsv(0, 255, 0)
    (120.0, 1.0, 1.0)
    >>> rgb_to_hsv(0, 0, 255)
    (240.0, 1.0, 1.0)
    >>> rgb_to_hsv(255, 255, 255)
    (0.0, 0.0, 1.0)
    >>> rgb_to_hsv(0, 0, 0)
    (0.0, 0.0, 0.0)
    >>> rgb_to_hsv(128, 128, 0)
    (60.0, 1.0, 0.50196)
    """
    if not all(0 <= c <= 255 for c in (red, green, blue)):
        raise ValueError("RGB values must be between 0 and 255")

    r, g, b = red / 255.0, green / 255.0, blue / 255.0
    max_c = max(r, g, b)
    min_c = min(r, g, b)
    diff = max_c - min_c

    # Hue
    if diff == 0:
        h = 0.0
    elif max_c == r:
        h = 60.0 * (((g - b) / diff) % 6)
    elif max_c == g:
        h = 60.0 * (((b - r) / diff) + 2)
    else:
        h = 60.0 * (((r - g) / diff) + 4)

    # Saturation
    s = 0.0 if max_c == 0 else diff / max_c

    # Value
    v = max_c

    return round(h, 5), round(s, 5), round(v, 5)


def hsv_to_rgb(hue: float, saturation: float, value: float) -> tuple[int, int, int]:
    """
    Convert HSV (H: 0-360, S: 0-1, V: 0-1) to RGB (0-255).

    >>> hsv_to_rgb(0, 1, 1)
    (255, 0, 0)
    >>> hsv_to_rgb(120, 1, 1)
    (0, 255, 0)
    >>> hsv_to_rgb(240, 1, 1)
    (0, 0, 255)
    >>> hsv_to_rgb(0, 0, 1)
    (255, 255, 255)
    >>> hsv_to_rgb(0, 0, 0)
    (0, 0, 0)
    """
    if not (0 <= hue <= 360 and 0 <= saturation <= 1 and 0 <= value <= 1):
        raise ValueError("Invalid HSV values")

    c = value * saturation
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = value - c

    if hue < 60:
        r, g, b = c, x, 0
    elif hue < 120:
        r, g, b = x, c, 0
    elif hue < 180:
        r, g, b = 0, c, x
    elif hue < 240:
        r, g, b = 0, x, c
    elif hue < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return (round((r + m) * 255), round((g + m) * 255), round((b + m) * 255))


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (128, 128, 0), (75, 0, 130)]
    for r, g, b in colors:
        h, s, v = rgb_to_hsv(r, g, b)
        back = hsv_to_rgb(h, s, v)
        print(f"  RGB({r},{g},{b}) -> HSV({h},{s},{v}) -> RGB{back}")
