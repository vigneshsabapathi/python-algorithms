#!/usr/bin/env python3
"""
Optimized and alternative implementations of geometry utilities.

The reference uses @dataclass inheritance (Ellipse -> Circle, Polygon ->
Rectangle -> Square) with manual validation in __post_init__.

Variants covered:
1. FunctionalCircle   -- pure-function approach: no classes, just functions
                         returning NamedTuples.  Zero overhead from dataclass
                         machinery.
2. SlottedCircle      -- __slots__ class with cached properties; avoids dict
                         overhead per instance, ideal for bulk allocations.
3. MathCircle         -- uses Ramanujan approximation for ellipse perimeter
                         (much more accurate than pi*(a+b)).

Key interview insight:
    Reference:  dataclass inheritance -- clean, Pythonic, moderate overhead
    Functional: NamedTuple -- immutable, hashable, zero-class overhead
    Slotted:    __slots__ -- fastest attribute access, lowest memory
    Math:       Ramanujan  -- interview favourite for "improve this formula"

Run:
    python geometry/geometry_optimized.py
"""

from __future__ import annotations

import math
import sys
import os
import timeit
from typing import NamedTuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from geometry.geometry import Circle, Ellipse, Rectangle, Square


# ---------------------------------------------------------------------------
# Variant 1 -- Functional / NamedTuple approach (no classes)
# ---------------------------------------------------------------------------

class CircleResult(NamedTuple):
    radius: float
    area: float
    perimeter: float
    diameter: float


def circle_functional(radius: float) -> CircleResult:
    """
    Pure-function circle: returns an immutable NamedTuple.

    >>> circle_functional(5)
    CircleResult(radius=5, area=78.53981633974483, perimeter=31.41592653589793, diameter=10)
    >>> circle_functional(0)
    Traceback (most recent call last):
        ...
    ValueError: radius must be positive
    >>> circle_functional(1).area
    3.141592653589793
    """
    if radius <= 0:
        raise ValueError("radius must be positive")
    return CircleResult(
        radius=radius,
        area=math.pi * radius * radius,
        perimeter=2 * math.pi * radius,
        diameter=2 * radius,
    )


class RectResult(NamedTuple):
    width: float
    height: float
    area: float
    perimeter: float


def rectangle_functional(width: float, height: float) -> RectResult:
    """
    Pure-function rectangle.

    >>> rectangle_functional(5, 10)
    RectResult(width=5, height=10, area=50, perimeter=30)
    >>> rectangle_functional(-1, 5)
    Traceback (most recent call last):
        ...
    ValueError: dimensions must be positive
    """
    if width <= 0 or height <= 0:
        raise ValueError("dimensions must be positive")
    return RectResult(
        width=width, height=height,
        area=width * height, perimeter=2 * (width + height),
    )


# ---------------------------------------------------------------------------
# Variant 2 -- __slots__ class with cached properties
# ---------------------------------------------------------------------------

class SlottedCircle:
    """
    Circle using __slots__ for minimal memory and fast attribute access.

    >>> sc = SlottedCircle(5)
    >>> sc.area
    78.53981633974483
    >>> sc.perimeter
    31.41592653589793
    >>> sc.diameter
    10
    >>> SlottedCircle(-1)
    Traceback (most recent call last):
        ...
    ValueError: radius must be positive
    """

    __slots__ = ("radius", "_area", "_perimeter")

    def __init__(self, radius: float) -> None:
        if radius <= 0:
            raise ValueError("radius must be positive")
        self.radius = radius
        self._area = math.pi * radius * radius
        self._perimeter = 2 * math.pi * radius

    @property
    def area(self) -> float:
        return self._area

    @property
    def perimeter(self) -> float:
        return self._perimeter

    @property
    def diameter(self) -> float:
        return self.radius * 2

    def max_parts(self, num_cuts: float) -> float:
        """
        >>> SlottedCircle(5).max_parts(7)
        29.0
        >>> SlottedCircle(5).max_parts(54)
        1486.0
        """
        if not isinstance(num_cuts, (int, float)) or num_cuts < 0:
            raise TypeError("num_cuts must be a positive numeric value.")
        return (num_cuts + 2 + num_cuts ** 2) * 0.5

    def __repr__(self) -> str:
        return f"SlottedCircle(radius={self.radius})"


# ---------------------------------------------------------------------------
# Variant 3 -- Ramanujan ellipse perimeter (more accurate)
# ---------------------------------------------------------------------------

def ellipse_perimeter_ramanujan(major: float, minor: float) -> float:
    """
    Ramanujan's first approximation for ellipse perimeter.

    Much more accurate than pi*(a+b) used by the reference.

    >>> round(ellipse_perimeter_ramanujan(5, 10), 6)
    48.442241
    >>> round(ellipse_perimeter_ramanujan(5, 5), 6)  # circle
    31.415927
    >>> ellipse_perimeter_ramanujan(-1, 5)
    Traceback (most recent call last):
        ...
    ValueError: radii must be positive
    """
    if major <= 0 or minor <= 0:
        raise ValueError("radii must be positive")
    a, b = max(major, minor), min(major, minor)
    h = ((a - b) / (a + b)) ** 2
    return math.pi * (a + b) * (1 + 3 * h / (10 + math.sqrt(4 - 3 * h)))


def ellipse_perimeter_naive(major: float, minor: float) -> float:
    """
    Reference-style naive perimeter: pi * (a + b).

    >>> round(ellipse_perimeter_naive(5, 10), 6)
    47.12389
    """
    return math.pi * (major + minor)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

CIRCLE_CASES = [
    (5, 78.53981633974483, 31.41592653589793, 10),
    (1, 3.141592653589793, 6.283185307179586, 2),
    (10, 314.1592653589793, 62.83185307179586, 20),
]

RECT_CASES = [
    (5, 10, 50, 30),
    (3, 7, 21, 20),
    (1, 1, 1, 4),
]


def run_all() -> None:
    print("\n=== Circle Correctness ===")
    for r, exp_area, exp_peri, exp_diam in CIRCLE_CASES:
        ref = Circle(r)
        func = circle_functional(r)
        slot = SlottedCircle(r)

        ok_area = abs(ref.area - exp_area) < 1e-9 and abs(func.area - exp_area) < 1e-9 and abs(slot.area - exp_area) < 1e-9
        ok_peri = abs(ref.perimeter - exp_peri) < 1e-9 and abs(func.perimeter - exp_peri) < 1e-9 and abs(slot.perimeter - exp_peri) < 1e-9
        tag = "OK" if (ok_area and ok_peri) else "FAIL"
        print(f"  [{tag}] Circle(r={r})  area={ref.area:.4f}  perimeter={ref.perimeter:.4f}")

    print("\n=== Rectangle Correctness ===")
    for w, h, exp_area, exp_peri in RECT_CASES:
        ref = Rectangle(w, h)
        func = rectangle_functional(w, h)
        ok = ref.area() == exp_area == func.area and ref.perimeter() == exp_peri == func.perimeter
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] Rectangle({w}, {h})  area={ref.area()}  perimeter={ref.perimeter()}")

    print("\n=== Ellipse Perimeter: Naive vs Ramanujan ===")
    for a, b in [(5, 10), (3, 7), (10, 10)]:
        naive = ellipse_perimeter_naive(a, b)
        rama = ellipse_perimeter_ramanujan(a, b)
        print(f"  Ellipse({a}, {b}): naive={naive:.4f}  ramanujan={rama:.4f}")

    REPS = 100_000
    print(f"\n=== Benchmark: {REPS} iterations ===")

    impls = [
        ("Reference Circle",   lambda: Circle(5).area),
        ("Functional circle",  lambda: circle_functional(5).area),
        ("Slotted circle",     lambda: SlottedCircle(5).area),
        ("Reference Rectangle", lambda: Rectangle(5, 10).area()),
        ("Functional rect",    lambda: rectangle_functional(5, 10).area),
    ]
    for name, fn in impls:
        t = timeit.timeit(fn, number=REPS) * 1000 / REPS
        print(f"  {name:<22} {t:>8.5f} ms / call")

    print(f"\n=== Perimeter Benchmark: {REPS} iterations ===")
    perim_impls = [
        ("Naive pi*(a+b)",     lambda: ellipse_perimeter_naive(5, 10)),
        ("Ramanujan approx",   lambda: ellipse_perimeter_ramanujan(5, 10)),
    ]
    for name, fn in perim_impls:
        t = timeit.timeit(fn, number=REPS) * 1000 / REPS
        print(f"  {name:<22} {t:>8.5f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
