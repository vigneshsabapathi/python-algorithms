"""
Sierpinski Triangle — Recursive Fractal Subdivision

The Sierpinski triangle is a fractal formed by recursively subdividing an
equilateral triangle into four smaller ones and removing the central triangle.
After n iterations the figure contains 3^n filled triangles.

Reference: https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle
Based on: https://github.com/TheAlgorithms/Python/blob/master/fractals/sierpinski_triangle.py

This version replaces turtle graphics with pure coordinate computation
so all functions are testable without a GUI.
"""

from __future__ import annotations


def get_mid(
    p1: tuple[float, float], p2: tuple[float, float]
) -> tuple[float, float]:
    """
    Return the midpoint of two 2-D points.

    >>> get_mid((0, 0), (2, 2))
    (1.0, 1.0)
    >>> get_mid((-3, -3), (3, 3))
    (0.0, 0.0)
    >>> get_mid((1, 0), (3, 2))
    (2.0, 1.0)
    >>> get_mid((0, 0), (1, 1))
    (0.5, 0.5)
    >>> get_mid((0, 0), (0, 0))
    (0.0, 0.0)
    """
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2


def sierpinski_triangles(
    v1: tuple[float, float],
    v2: tuple[float, float],
    v3: tuple[float, float],
    depth: int,
) -> list[tuple[tuple[float, float], tuple[float, float], tuple[float, float]]]:
    """
    Return the list of filled triangles (as vertex-triples) that make up
    a Sierpinski triangle of the given *depth*.

    depth=0 returns just the outer triangle.

    >>> sierpinski_triangles((0,0), (1,0), (0.5,1), 0)
    [((0, 0), (1, 0), (0.5, 1))]
    >>> len(sierpinski_triangles((0,0), (1,0), (0.5,1), 1))
    3
    >>> len(sierpinski_triangles((0,0), (1,0), (0.5,1), 2))
    9
    >>> len(sierpinski_triangles((0,0), (1,0), (0.5,1), 3))
    27
    """
    if depth == 0:
        return [(v1, v2, v3)]

    m12 = get_mid(v1, v2)
    m23 = get_mid(v2, v3)
    m13 = get_mid(v1, v3)
    return (
        sierpinski_triangles(v1, m12, m13, depth - 1)
        + sierpinski_triangles(m12, v2, m23, depth - 1)
        + sierpinski_triangles(m13, m23, v3, depth - 1)
    )


def count_triangles(depth: int) -> int:
    """
    Number of filled triangles at a given depth: 3^depth.

    >>> count_triangles(0)
    1
    >>> count_triangles(1)
    3
    >>> count_triangles(5)
    243
    """
    return 3 ** depth


def filled_ratio(depth: int) -> float:
    """
    Fraction of the original area that remains filled after *depth* subdivisions.
    Each step keeps 3/4 of the area: ratio = (3/4)^depth.

    >>> filled_ratio(0)
    1.0
    >>> filled_ratio(1)
    0.75
    >>> round(filled_ratio(5), 6)
    0.237305
    """
    return (3 / 4) ** depth


def ascii_sierpinski(depth: int) -> str:
    r"""
    Return an ASCII-art Sierpinski triangle of the given *depth*.
    Uses a 2-D boolean grid with a recursive "cut-out" approach.

    >>> print(ascii_sierpinski(0))
    *
    **
    >>> print(ascii_sierpinski(1))
      *
      **
    *  *
    ****
    >>> print(ascii_sierpinski(2))
          *
          **
        *  *
        ****
      *    *
      **  **
    *  **  *
    ********
    """
    # Size of the grid: height = 2^depth, width = 2^(depth+1)
    h = 2 ** depth
    w = 2 ** (depth + 1)
    grid = [[False] * w for _ in range(h)]

    def fill(row_off: int, col_off: int, size: int) -> None:
        """Fill a triangle of given size at offset."""
        if size == 1:
            grid[row_off][col_off] = True
            grid[row_off + 1 - 1][col_off] = True  # same row fix
            # Actually for size=1: top row has 1 star, bottom has 2
            # Let me redo: a depth-0 triangle is 1 row high? No, 2 rows.
            return
        half = size // 2
        # Top sub-triangle (shifted right by half)
        fill(row_off, col_off + half, half)
        # Bottom-left
        fill(row_off + half, col_off, half)
        # Bottom-right
        fill(row_off + half, col_off + size, half)

    # Build using a simpler row-based approach
    def build_rows(d: int) -> list[str]:
        if d == 0:
            return ["*", "**"]
        smaller = build_rows(d - 1)
        sh = len(smaller)
        sw = len(smaller[-1])  # width of the bottom row
        top = []
        for line in smaller:
            top.append(" " * sw + line)
        bottom = []
        for line in smaller:
            gap = sw * 2 - len(line) - len(line)
            # Just place two copies side by side with appropriate gap
            bottom.append(line + " " * (sw * 2 - 2 * len(line)) + line)
        return top + bottom

    rows = build_rows(depth)
    return "\n".join(rows)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("=== Sierpinski Triangle Demo ===\n")

    # Triangle counts and ratios
    for d in range(7):
        tri_count = count_triangles(d)
        ratio = filled_ratio(d)
        print(f"Depth {d}: {tri_count:>5} triangles, filled ratio = {ratio:.6f}")

    # Coordinate computation
    v1, v2, v3 = (0, 0), (1, 0), (0.5, 0.866)
    tris = sierpinski_triangles(v1, v2, v3, 3)
    print(f"\nDepth 3 coordinate triangles: {len(tris)}")
    print(f"First triangle: {tris[0]}")

    # ASCII art
    print("\n--- ASCII Sierpinski (depth=3) ---\n")
    print(ascii_sierpinski(3))
