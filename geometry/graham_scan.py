# https://github.com/TheAlgorithms/Python/blob/master/geometry/graham_scan.py
"""
Graham Scan algorithm for computing the convex hull of a set of 2-D points.

The algorithm finds all vertices of the convex hull ordered along its boundary
in O(n log n) time by:
  1. Choosing the bottom-most (then left-most) anchor point.
  2. Sorting remaining points by polar angle relative to the anchor.
  3. Processing sorted points with a stack, discarding clockwise turns.

Reference:
  Graham, R.L. (1972). "An Efficient Algorithm for Determining the Convex Hull
  of a Finite Planar Set"
  https://en.wikipedia.org/wiki/Graham_scan
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cmp_to_key


class Point:
    """
    A point in 2-D space.

    >>> Point(0, 0)
    Point(x=0.0, y=0.0)
    >>> Point(1.5, 2.5)
    Point(x=1.5, y=2.5)
    >>> Point(1, 2) == Point(1, 2)
    True
    >>> Point(1, 2) == Point(2, 1)
    False
    """

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    # -- comparison / hashing --------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: Point) -> bool:
        """
        Bottom-most first, then left-most.

        >>> Point(1, 2) < Point(1, 3)
        True
        >>> Point(1, 2) < Point(2, 2)
        True
        """
        return (self.y, self.x) < (other.y, other.x)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    # -- geometry helpers ------------------------------------------------------

    def distance_to(self, other: Point) -> float:
        """
        Euclidean distance.

        >>> Point(0, 0).distance_to(Point(3, 4))
        5.0
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    @staticmethod
    def cross(o: Point, a: Point, b: Point) -> float:
        """
        Cross product of vectors OA and OB.

        Positive  -> counter-clockwise (left turn)
        Negative  -> clockwise (right turn)
        Zero      -> collinear

        >>> Point.cross(Point(0, 0), Point(1, 0), Point(1, 1))
        1.0
        >>> Point.cross(Point(0, 0), Point(1, 0), Point(1, -1))
        -1.0
        >>> Point.cross(Point(0, 0), Point(1, 0), Point(2, 0))
        0.0
        """
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


def graham_scan(points: Sequence[Point]) -> list[Point]:
    """
    Compute the convex hull using Graham Scan.

    Returns hull vertices in counter-clockwise order, or [] if fewer than
    3 non-collinear points exist.

    Time:  O(n log n)  (sorting dominates)
    Space: O(n)

    >>> graham_scan([])
    []
    >>> graham_scan([Point(0, 0)])
    []
    >>> graham_scan([Point(0, 0), Point(1, 1)])
    []
    >>> hull = graham_scan([Point(0,0), Point(1,0), Point(0.5,1)])
    >>> len(hull)
    3
    >>> all(p in hull for p in [Point(0,0), Point(1,0), Point(0.5,1)])
    True
    >>> hull = graham_scan([
    ...     Point(0,0), Point(2,0), Point(2,2), Point(0,2), Point(1,1)
    ... ])
    >>> len(hull)
    4
    >>> Point(1,1) in hull  # interior point excluded
    False
    """
    if len(points) < 3:
        return []

    # 1. Bottom-most, then left-most anchor
    anchor = min(points)

    # 2. Sort by polar angle relative to anchor
    rest = [p for p in points if p != anchor]
    if not rest:
        return []

    def _cmp(a: Point, b: Point) -> int:
        cross = Point.cross(anchor, a, b)
        if cross > 0:
            return -1          # a before b (CCW)
        if cross < 0:
            return 1           # a after b  (CW)
        # Collinear: closer point first
        da = anchor.distance_to(a)
        db = anchor.distance_to(b)
        return -1 if da < db else (1 if da > db else 0)

    rest.sort(key=cmp_to_key(_cmp))

    # 3. Build hull with a stack
    stack: list[Point] = [anchor, rest[0]]

    for p in rest[1:]:
        while len(stack) >= 2 and Point.cross(stack[-2], stack[-1], p) <= 0:
            stack.pop()
        stack.append(p)

    return stack if len(stack) >= 3 else []


# ── Demo / self-test ──────────────────────────────────────────────────────────

def _demo() -> None:
    test_sets = [
        (
            "square + interior",
            [Point(0,0), Point(2,0), Point(2,2), Point(0,2), Point(1,1)],
        ),
        (
            "grid 3x3",
            [Point(x,y) for x in range(3) for y in range(3)],
        ),
        (
            "triangle",
            [Point(0,0), Point(4,0), Point(2,3)],
        ),
        (
            "collinear",
            [Point(0,0), Point(1,1), Point(2,2)],
        ),
    ]

    for label, pts in test_sets:
        hull = graham_scan(pts)
        coords = [(p.x, p.y) for p in hull]
        print(f"  {label:20s} -> {len(hull)} hull pts: {coords}")


if __name__ == "__main__":
    import doctest

    results = doctest.testmod(verbose=False)
    print(f"Doctests: {results.attempted} run, {results.failed} failed.")
    print("\n=== Graham Scan Demo ===")
    _demo()
