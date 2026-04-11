"""
Vicsek Fractal — Recursive Cross-Shaped Subdivision

The Vicsek fractal is built by dividing a square into a 3x3 grid and keeping
only the center cell plus the four edge-adjacent cells (forming a plus/cross
shape).  This is repeated recursively.  The fractal dimension is
log(5)/log(3) ~ 1.465.

Reference: https://en.wikipedia.org/wiki/Vicsek_fractal
Based on: https://github.com/TheAlgorithms/Python/blob/master/fractals/vicsek.py

This version replaces turtle graphics with pure coordinate computation.
"""

from __future__ import annotations


def vicsek_cells(
    x: float, y: float, length: float, depth: int
) -> list[tuple[float, float, float]]:
    """
    Return the list of (center_x, center_y, cell_size) for all filled cells
    in a Vicsek fractal of given depth centered at (x, y) with the given length.

    depth=0 returns just the single cross.

    >>> vicsek_cells(0, 0, 9, 0)
    [(0, 0, 9)]
    >>> len(vicsek_cells(0, 0, 9, 1))
    5
    >>> len(vicsek_cells(0, 0, 9, 2))
    25
    >>> len(vicsek_cells(0, 0, 9, 3))
    125
    """
    if depth == 0:
        return [(x, y, length)]
    sub = length / 3
    return (
        vicsek_cells(x, y, sub, depth - 1)              # center
        + vicsek_cells(x + length / 3, y, sub, depth - 1)  # right
        + vicsek_cells(x - length / 3, y, sub, depth - 1)  # left
        + vicsek_cells(x, y + length / 3, sub, depth - 1)  # up
        + vicsek_cells(x, y - length / 3, sub, depth - 1)  # down
    )


def count_cells(depth: int) -> int:
    """
    Number of filled cells at a given depth: 5^depth.

    >>> count_cells(0)
    1
    >>> count_cells(1)
    5
    >>> count_cells(4)
    625
    """
    return 5 ** depth


def fractal_dimension() -> float:
    """
    The Hausdorff dimension of the Vicsek fractal: log(5)/log(3).

    >>> round(fractal_dimension(), 4)
    1.465
    """
    import math

    return math.log(5) / math.log(3)


def filled_ratio(depth: int) -> float:
    """
    Fraction of the bounding square that is filled at *depth*.
    Each step keeps 5 out of 9 sub-squares: (5/9)^depth.

    >>> filled_ratio(0)
    1.0
    >>> round(filled_ratio(1), 6)
    0.555556
    >>> round(filled_ratio(3), 6)
    0.171468
    """
    return (5 / 9) ** depth


def ascii_vicsek(depth: int) -> str:
    """
    Return an ASCII-art rendering of a Vicsek fractal.
    Grid size is 3^depth x 3^depth.

    >>> print(ascii_vicsek(0))
    #
    >>> print(ascii_vicsek(1))
    .#.
    ###
    .#.
    >>> art = ascii_vicsek(2)
    >>> art.count('#')
    25
    >>> len(art.splitlines())
    9
    """
    size = 3 ** depth
    grid = [[False] * size for _ in range(size)]

    def fill(cx: int, cy: int, s: int, d: int) -> None:
        """Mark filled cells recursively. cx, cy = top-left corner."""
        if d == 0:
            grid[cy][cx] = True
            return
        third = s // 3
        # center
        fill(cx + third, cy + third, third, d - 1)
        # right
        fill(cx + 2 * third, cy + third, third, d - 1)
        # left
        fill(cx, cy + third, third, d - 1)
        # top
        fill(cx + third, cy, third, d - 1)
        # bottom
        fill(cx + third, cy + 2 * third, third, d - 1)

    fill(0, 0, size, depth)
    lines = []
    for row in grid:
        lines.append("".join("#" if c else "." for c in row))
    return "\n".join(lines)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("=== Vicsek Fractal Demo ===\n")

    print(f"Hausdorff dimension: {fractal_dimension():.6f}")
    print()

    for d in range(6):
        cells = count_cells(d)
        ratio = filled_ratio(d)
        grid_size = 3 ** d
        print(
            f"Depth {d}: {cells:>6} cells, "
            f"grid {grid_size:>4}x{grid_size:<4}, "
            f"filled = {ratio:.6f}"
        )

    print("\n--- ASCII Vicsek (depth=2) ---\n")
    print(ascii_vicsek(2))

    print("\n--- ASCII Vicsek (depth=3) ---\n")
    print(ascii_vicsek(3))
