"""
Points Are Collinear in 3D
==========================
Three points a, b, c are collinear iff the vectors (b-a) and (c-a) are
parallel, i.e. their cross product has zero magnitude.
"""
from typing import Sequence

Point3 = Sequence[float]


def _sub(p: Point3, q: Point3) -> tuple[float, float, float]:
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def _cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def are_collinear(a: Point3, b: Point3, c: Point3, tol: float = 1e-9) -> bool:
    """
    >>> are_collinear((0,0,0), (1,1,1), (2,2,2))
    True
    >>> are_collinear((0,0,0), (1,0,0), (0,1,0))
    False
    >>> are_collinear((1,2,3), (4,5,6), (7,8,9))
    True
    >>> are_collinear((0,0,0), (0,0,0), (1,1,1))
    True
    """
    ab = _sub(b, a)
    ac = _sub(c, a)
    cx, cy, cz = _cross(ab, ac)
    return abs(cx) <= tol and abs(cy) <= tol and abs(cz) <= tol


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    tests = [
        ((0, 0, 0), (1, 1, 1), (2, 2, 2)),
        ((0, 0, 0), (1, 0, 0), (0, 1, 0)),
        ((1, 2, 3), (4, 5, 6), (7, 8, 9)),
    ]
    for a, b, c in tests:
        print(f"{a}, {b}, {c} -> {are_collinear(a, b, c)}")
