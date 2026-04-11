"""
Mirror Formulae (Spherical Mirror Equation).

    1/f = 1/v + 1/u

where (using sign convention):
    f = focal length (m) — positive for concave, negative for convex
    v = image distance (m)
    u = object distance (m) — always negative (object in front of mirror)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/mirror_formulae.py
"""


def focal_length(object_distance: float, image_distance: float) -> float:
    """
    Calculate focal length of a mirror.

    1/f = 1/v + 1/u  =>  f = (u * v) / (u + v)

    >>> round(focal_length(-20, -30), 4)
    -12.0
    >>> round(focal_length(-10, -20), 4)
    -6.6667
    >>> focal_length(0, 10)
    Traceback (most recent call last):
        ...
    ValueError: object_distance must not be zero
    """
    if object_distance == 0:
        raise ValueError("object_distance must not be zero")
    if image_distance == 0:
        raise ValueError("image_distance must not be zero")
    if object_distance + image_distance == 0:
        raise ValueError("object and image distances sum to zero")

    return (object_distance * image_distance) / (object_distance + image_distance)


def image_distance(focal_len: float, object_distance: float) -> float:
    """
    Calculate image distance.

    1/v = 1/f - 1/u  =>  v = (f * u) / (u - f)

    >>> round(image_distance(12, -20), 4)
    7.5
    """
    if focal_len == 0:
        raise ValueError("focal_length must not be zero")
    if object_distance == 0:
        raise ValueError("object_distance must not be zero")
    if object_distance == focal_len:
        raise ValueError("object at focal point produces image at infinity")

    return (focal_len * object_distance) / (object_distance - focal_len)


def object_distance(focal_len: float, image_dist: float) -> float:
    """
    Calculate object distance.

    1/u = 1/f - 1/v  =>  u = (f * v) / (v - f)

    >>> round(object_distance(12, -7.5), 4)
    4.6154
    """
    if focal_len == 0:
        raise ValueError("focal_length must not be zero")
    if image_dist == 0:
        raise ValueError("image_distance must not be zero")
    if image_dist == focal_len:
        raise ValueError("image at focal point implies object at infinity")

    return (focal_len * image_dist) / (image_dist - focal_len)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
