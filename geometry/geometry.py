# https://github.com/TheAlgorithms/Python/blob/master/geometry/geometry.py
"""
Basic geometry utilities: Angle, Side, Ellipse, Circle, Polygon, Rectangle, Square.

Provides building-block dataclasses for 2-D computational geometry with full
input validation and doctests.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from types import NoneType
from typing import Self


# ── Building-block classes ────────────────────────────────────────────────────


@dataclass
class Angle:
    """
    An angle measured in degrees (0-360 inclusive).

    >>> Angle()
    Angle(degrees=90)
    >>> Angle(45.5)
    Angle(degrees=45.5)
    >>> Angle(-1)
    Traceback (most recent call last):
        ...
    TypeError: degrees must be a numeric value between 0 and 360.
    >>> Angle(361)
    Traceback (most recent call last):
        ...
    TypeError: degrees must be a numeric value between 0 and 360.
    """

    degrees: float = 90

    def __post_init__(self) -> None:
        if not isinstance(self.degrees, (int, float)) or not 0 <= self.degrees <= 360:
            raise TypeError("degrees must be a numeric value between 0 and 360.")


@dataclass
class Side:
    """
    A side of a 2-D polygon with length, angle to next side, and optional link.

    >>> Side(5)
    Side(length=5, angle=Angle(degrees=90), next_side=None)
    >>> Side(5, Angle(45.6))
    Side(length=5, angle=Angle(degrees=45.6), next_side=None)
    >>> Side(5, Angle(45.6), Side(1, Angle(2)))  # doctest: +ELLIPSIS
    Side(length=5, angle=Angle(degrees=45.6), next_side=Side(length=1, angle=Angle(d...
    >>> Side(-1)
    Traceback (most recent call last):
        ...
    TypeError: length must be a positive numeric value.
    >>> Side(5, None)
    Traceback (most recent call last):
        ...
    TypeError: angle must be an Angle object.
    >>> Side(5, Angle(90), "Invalid next_side")
    Traceback (most recent call last):
        ...
    TypeError: next_side must be a Side or None.
    """

    length: float
    angle: Angle = field(default_factory=Angle)
    next_side: Side | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.length, (int, float)) or self.length <= 0:
            raise TypeError("length must be a positive numeric value.")
        if not isinstance(self.angle, Angle):
            raise TypeError("angle must be an Angle object.")
        if not isinstance(self.next_side, (Side, NoneType)):
            raise TypeError("next_side must be a Side or None.")


# ── Curves ────────────────────────────────────────────────────────────────────


@dataclass
class Ellipse:
    """
    A geometric ellipse defined by major and minor radii.

    >>> Ellipse(5, 10)
    Ellipse(major_radius=5, minor_radius=10)
    >>> Ellipse(5, 10) == Ellipse(5, 10)
    True
    """

    major_radius: float
    minor_radius: float

    @property
    def area(self) -> float:
        """
        >>> Ellipse(5, 10).area
        157.07963267948966
        """
        return math.pi * self.major_radius * self.minor_radius

    @property
    def perimeter(self) -> float:
        """
        Approximate perimeter (pi * sum of radii).

        >>> Ellipse(5, 10).perimeter
        47.12388980384689
        """
        return math.pi * (self.major_radius + self.minor_radius)


class Circle(Ellipse):
    """
    A circle — special case of Ellipse where both radii are equal.

    >>> Circle(5)
    Circle(radius=5)
    >>> Circle(5) == Circle(5)
    True
    >>> Circle(5).area
    78.53981633974483
    >>> Circle(5).perimeter
    31.41592653589793
    """

    def __init__(self, radius: float) -> None:
        super().__init__(radius, radius)
        self.radius = radius

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius})"

    @property
    def diameter(self) -> float:
        """
        >>> Circle(5).diameter
        10
        """
        return self.radius * 2

    def max_parts(self, num_cuts: float) -> float:
        """
        Maximum regions a circle can be divided into with *num_cuts* straight cuts
        (lazy caterer's sequence).

        >>> c = Circle(5)
        >>> c.max_parts(0)
        1.0
        >>> c.max_parts(7)
        29.0
        >>> c.max_parts(54)
        1486.0
        >>> c.max_parts(22.5)
        265.375
        >>> c.max_parts(-222)
        Traceback (most recent call last):
            ...
        TypeError: num_cuts must be a positive numeric value.
        >>> c.max_parts("-222")
        Traceback (most recent call last):
            ...
        TypeError: num_cuts must be a positive numeric value.
        """
        if not isinstance(num_cuts, (int, float)) or num_cuts < 0:
            raise TypeError("num_cuts must be a positive numeric value.")
        return (num_cuts + 2 + num_cuts**2) * 0.5


# ── Polygons ──────────────────────────────────────────────────────────────────


@dataclass
class Polygon:
    """
    Generic polygon stored as a list of Side objects.

    >>> Polygon()
    Polygon(sides=[])
    >>> p = Polygon()
    >>> p.add_side(Side(5)).get_side(0)
    Side(length=5, angle=Angle(degrees=90), next_side=None)
    >>> p.get_side(1)
    Traceback (most recent call last):
        ...
    IndexError: list index out of range
    >>> p.set_side(0, Side(10)).get_side(0)
    Side(length=10, angle=Angle(degrees=90), next_side=None)
    >>> p.set_side(1, Side(10))
    Traceback (most recent call last):
        ...
    IndexError: list assignment index out of range
    """

    sides: list[Side] = field(default_factory=list)

    def add_side(self, side: Side) -> Self:
        """
        >>> Polygon().add_side(Side(5))
        Polygon(sides=[Side(length=5, angle=Angle(degrees=90), next_side=None)])
        """
        self.sides.append(side)
        return self

    def get_side(self, index: int) -> Side:
        """
        >>> Polygon().get_side(0)
        Traceback (most recent call last):
            ...
        IndexError: list index out of range
        >>> Polygon().add_side(Side(5)).get_side(-1)
        Side(length=5, angle=Angle(degrees=90), next_side=None)
        """
        return self.sides[index]

    def set_side(self, index: int, side: Side) -> Self:
        """
        >>> Polygon().set_side(0, Side(5))
        Traceback (most recent call last):
            ...
        IndexError: list assignment index out of range
        >>> Polygon().add_side(Side(5)).set_side(0, Side(10))
        Polygon(sides=[Side(length=10, angle=Angle(degrees=90), next_side=None)])
        """
        self.sides[index] = side
        return self


class Rectangle(Polygon):
    """
    Rectangle with short and long sides.

    >>> r = Rectangle(5, 10)
    >>> r.perimeter()
    30
    >>> r.area()
    50
    >>> Rectangle(-5, 10)
    Traceback (most recent call last):
        ...
    TypeError: length must be a positive numeric value.
    """

    def __init__(self, short_side_length: float, long_side_length: float) -> None:
        super().__init__()
        self.short_side_length = short_side_length
        self.long_side_length = long_side_length
        self._build_sides()

    def _build_sides(self) -> None:
        """
        >>> Rectangle(5, 10)  # doctest: +NORMALIZE_WHITESPACE
        Rectangle(sides=[Side(length=5, angle=Angle(degrees=90), next_side=None),
        Side(length=10, angle=Angle(degrees=90), next_side=None)])
        """
        self.short_side = Side(self.short_side_length)
        self.long_side = Side(self.long_side_length)
        super().add_side(self.short_side)
        super().add_side(self.long_side)

    def perimeter(self) -> float:
        return (self.short_side.length + self.long_side.length) * 2

    def area(self) -> float:
        return self.short_side.length * self.long_side.length


@dataclass
class Square(Rectangle):
    """
    Square — Rectangle with equal sides.

    >>> s = Square(5)
    >>> s.perimeter()
    20
    >>> s.area()
    25
    """

    def __init__(self, side_length: float) -> None:
        super().__init__(side_length, side_length)

    def perimeter(self) -> float:
        return super().perimeter()

    def area(self) -> float:
        return super().area()


# ── Demo / self-test ──────────────────────────────────────────────────────────


def _demo() -> None:
    """Quick showcase of every class."""
    print("=== Geometry Utilities Demo ===\n")

    a = Angle(60)
    print(f"Angle:       {a}")

    s = Side(7, Angle(45))
    print(f"Side:        {s}")

    e = Ellipse(5, 10)
    print(f"Ellipse:     {e}  area={e.area:.4f}  perimeter={e.perimeter:.4f}")

    c = Circle(5)
    print(
        f"Circle:      {c}  area={c.area:.4f}  perimeter={c.perimeter:.4f}  "
        f"diameter={c.diameter}"
    )
    print(f"  max_parts(7)  = {c.max_parts(7)}")
    print(f"  max_parts(54) = {c.max_parts(54)}")

    r = Rectangle(5, 10)
    print(f"Rectangle:   perimeter={r.perimeter()}  area={r.area()}")

    sq = Square(5)
    print(f"Square:      perimeter={sq.perimeter()}  area={sq.area()}")


if __name__ == "__main__":
    import doctest

    results = doctest.testmod(verbose=False)
    print(f"Doctests: {results.attempted} run, {results.failed} failed.")
    _demo()
