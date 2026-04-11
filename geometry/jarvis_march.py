# https://github.com/TheAlgorithms/Python/blob/master/geometry/jarvis_march.py
"""
Jarvis March (Gift Wrapping) algorithm for computing the convex hull.

Starts at the leftmost point and repeatedly selects the most counter-clockwise
point until wrapping back to the start.

Time:  O(n * h)  where h = number of hull vertices
Space: O(h)

Best when h is small (output-sensitive); worst-case O(n^2) when all points are
on the hull.

Reference:
  https://en.wikipedia.org/wiki/Gift_wrapping_algorithm
"""

from __future__ import annotations


class Point:
    """
    A 2-D point.

    >>> Point(0, 0)
    Point(0, 0)
    >>> Point(1, 2) == Point(1, 2)
    True
    >>> Point(1, 2) == Point(2, 1)
    False
    """

    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


def _cross(o: Point, a: Point, b: Point) -> float:
    """
    Cross product of vectors OA x OB.

    >0 : counter-clockwise  (left turn)
     0 : collinear
    <0 : clockwise           (right turn)

    >>> _cross(Point(0,0), Point(1,0), Point(0,1))
    1
    >>> _cross(Point(0,0), Point(1,0), Point(2,0))
    0
    >>> _cross(Point(0,0), Point(0,1), Point(1,0))
    -1
    """
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


def _dist_sq(a: Point, b: Point) -> float:
    """Squared Euclidean distance (avoids sqrt)."""
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2


def jarvis_march(points: list[Point]) -> list[Point]:
    """
    Convex hull via Jarvis March / Gift Wrapping.

    Returns hull vertices in counter-clockwise order starting from the
    leftmost (bottom-most tie-break) point, or [] if fewer than 3
    non-collinear points.

    >>> jarvis_march([])
    []
    >>> jarvis_march([Point(0,0), Point(1,1)])
    []
    >>> hull = jarvis_march([Point(0,0), Point(1,0), Point(0.5,1)])
    >>> len(hull)
    3
    >>> hull = jarvis_march([
    ...     Point(0,0), Point(2,0), Point(2,2), Point(0,2), Point(1,1)
    ... ])
    >>> len(hull)
    4
    >>> Point(1,1) in hull  # interior point excluded
    False
    >>> jarvis_march([Point(0,0), Point(1,1), Point(2,2)])  # collinear
    []
    """
    n = len(points)
    if n < 3:
        return []

    # Remove duplicates
    unique = list({(p.x, p.y): p for p in points}.values())
    n = len(unique)
    if n < 3:
        return []

    # Start from leftmost (bottom-most tie-break)
    start = min(range(n), key=lambda i: (unique[i].x, unique[i].y))

    hull: list[Point] = []
    current = start

    while True:
        hull.append(unique[current])
        candidate = 0 if current != 0 else 1

        for i in range(n):
            if i == current:
                continue
            cross = _cross(unique[current], unique[candidate], unique[i])
            if cross < 0:
                # i is more counter-clockwise
                candidate = i
            elif cross == 0:
                # Collinear: pick the farther point
                if _dist_sq(unique[current], unique[i]) > _dist_sq(
                    unique[current], unique[candidate]
                ):
                    candidate = i

        current = candidate
        if current == start:
            break

        # Safety: hull can't have more points than input
        if len(hull) > n:
            break

    return hull if len(hull) >= 3 else []


# ── Demo / self-test ──────────────────────────────────────────────────────────

def _demo() -> None:
    test_sets = [
        (
            "square + interior",
            [Point(0,0), Point(2,0), Point(2,2), Point(0,2), Point(1,1)],
        ),
        (
            "pentagon",
            [Point(0,1), Point(1,0), Point(2,0), Point(3,1), Point(1.5,3), Point(1.5,1)],
        ),
        (
            "collinear",
            [Point(0,0), Point(1,1), Point(2,2)],
        ),
        (
            "duplicates",
            [Point(0,0), Point(0,0), Point(1,0), Point(0,1)],
        ),
    ]

    for label, pts in test_sets:
        hull = jarvis_march(pts)
        coords = [(p.x, p.y) for p in hull]
        print(f"  {label:20s} -> {len(hull)} hull pts: {coords}")


if __name__ == "__main__":
    import doctest

    results = doctest.testmod(verbose=False)
    print(f"Doctests: {results.attempted} run, {results.failed} failed.")
    print("\n=== Jarvis March Demo ===")
    _demo()
