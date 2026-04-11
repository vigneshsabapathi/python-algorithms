"""
Mandelbrot Set — Escape-Time Algorithm

The Mandelbrot set is the set of complex numbers c for which the iteration
z_(n+1) = z_n^2 + c (starting from z_0 = 0) does not diverge.  A point
diverges if |z_n| > 2.  The "escape time" (number of iterations before
divergence) is used for color-coding visualizations.

Reference: https://en.wikipedia.org/wiki/Mandelbrot_set
Based on: https://github.com/TheAlgorithms/Python/blob/master/fractals/mandelbrot.py

This version keeps the computation pure (no PIL/matplotlib needed for doctests).
"""

import colorsys


def get_distance(x: float, y: float, max_step: int) -> float:
    """
    Return the *relative* escape step (step / (max_step-1)) for the point
    c = x + yi.  Points inside the Mandelbrot set return 1.0.

    >>> get_distance(0, 0, 50)
    1.0
    >>> get_distance(0.5, 0.5, 50)
    0.061224489795918366
    >>> get_distance(2, 0, 50)
    0.0
    """
    a, b = x, y
    for step in range(max_step):  # noqa: B007
        a_new = a * a - b * b + x
        b = 2 * a * b + y
        a = a_new
        if a * a + b * b > 4:
            break
    return step / (max_step - 1)


def get_black_and_white_rgb(distance: float) -> tuple[int, int, int]:
    """
    Black for Mandelbrot members (distance == 1), white otherwise.

    >>> get_black_and_white_rgb(0)
    (255, 255, 255)
    >>> get_black_and_white_rgb(0.5)
    (255, 255, 255)
    >>> get_black_and_white_rgb(1)
    (0, 0, 0)
    """
    return (0, 0, 0) if distance == 1 else (255, 255, 255)


def get_color_coded_rgb(distance: float) -> tuple[int, int, int]:
    """
    HSV-based color for escaped points; black for Mandelbrot members.

    >>> get_color_coded_rgb(0)
    (255, 0, 0)
    >>> get_color_coded_rgb(0.5)
    (0, 255, 255)
    >>> get_color_coded_rgb(1)
    (0, 0, 0)
    """
    if distance == 1:
        return (0, 0, 0)
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(distance, 1, 1))


def escape_time(x: float, y: float, max_iter: int) -> int:
    """
    Return the raw iteration count at which c = x + yi escapes.
    Returns max_iter if it never escapes (member of the set).

    >>> escape_time(0, 0, 100)
    100
    >>> escape_time(2, 0, 100)
    2
    >>> escape_time(0.5, 0.5, 100)
    5
    """
    a, b = 0.0, 0.0
    for n in range(1, max_iter + 1):
        a, b = a * a - b * b + x, 2 * a * b + y
        if a * a + b * b > 4:
            return n
    return max_iter


def is_in_mandelbrot(x: float, y: float, max_iter: int = 100) -> bool:
    """
    Check if c = x + yi is in the Mandelbrot set (does not escape
    within max_iter iterations).

    >>> is_in_mandelbrot(0, 0)
    True
    >>> is_in_mandelbrot(0.25, 0)
    True
    >>> is_in_mandelbrot(2, 0)
    False
    >>> is_in_mandelbrot(-1, 0)
    True
    """
    return escape_time(x, y, max_iter) == max_iter


def compute_mandelbrot_grid(
    x_min: float = -2.0,
    x_max: float = 0.5,
    y_min: float = -1.25,
    y_max: float = 1.25,
    width: int = 10,
    height: int = 10,
    max_iter: int = 50,
) -> list[list[int]]:
    """
    Compute an escape-time grid for the given region of the complex plane.
    Returns a 2-D list of iteration counts (height rows x width cols).

    >>> grid = compute_mandelbrot_grid(width=5, height=5, max_iter=20)
    >>> len(grid), len(grid[0])
    (5, 5)
    >>> grid[0][0]  # top-left corner at (-2, 1.25) -- escapes quickly
    1
    """
    dx = (x_max - x_min) / (width - 1) if width > 1 else 0
    dy = (y_max - y_min) / (height - 1) if height > 1 else 0
    grid: list[list[int]] = []
    for row in range(height):
        y = y_max - row * dy
        line: list[int] = []
        for col in range(width):
            x = x_min + col * dx
            line.append(escape_time(x, y, max_iter))
        grid.append(line)
    return grid


def ascii_mandelbrot(
    width: int = 72,
    height: int = 24,
    max_iter: int = 50,
) -> str:
    """
    Return an ASCII-art rendering of the Mandelbrot set.
    Characters represent escape-time bands.

    >>> art = ascii_mandelbrot(20, 10, 30)
    >>> len(art.splitlines())
    10
    """
    chars = " .:-=+*#%@"
    grid = compute_mandelbrot_grid(
        x_min=-2.0, x_max=0.5, y_min=-1.25, y_max=1.25,
        width=width, height=height, max_iter=max_iter,
    )
    lines: list[str] = []
    for row in grid:
        line = ""
        for val in row:
            idx = int((val / max_iter) * (len(chars) - 1))
            line += chars[idx]
        lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("=== Mandelbrot Set Demo ===\n")

    # Test key points
    test_points = [
        (0, 0, "origin"),
        (-1, 0, "period-2 bulb"),
        (0.25, 0, "cusp"),
        (0.5, 0.5, "outside"),
        (2, 0, "far outside"),
        (-0.75, 0, "main cardioid edge"),
    ]
    for x, y, label in test_points:
        et = escape_time(x, y, 100)
        member = "IN" if et == 100 else f"OUT (escaped at {et})"
        print(f"  c = {x:+.2f}{y:+.2f}i [{label:>20s}] -> {member}")

    print(f"\n--- ASCII Mandelbrot (72 x 24) ---\n")
    print(ascii_mandelbrot())
