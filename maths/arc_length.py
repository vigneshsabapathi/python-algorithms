from math import pi


def arc_length(angle: int, radius: int) -> float:
    """
    Computes the arc length s of a circular sector:
        s = 2 * pi * r * (angle / 360)
    where `angle` is in degrees and `radius` is in any length unit.

    >>> arc_length(45, 5)
    3.9269908169872414
    >>> arc_length(120, 15)
    31.415926535897928
    >>> arc_length(90, 10)
    15.707963267948966
    """
    return 2 * pi * radius * (angle / 360)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(arc_length(90, 10))
