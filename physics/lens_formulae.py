"""
Lens Formulae (Thin Lens Equation).

    1/f = 1/v - 1/u

where:
    f = focal length (m)
    v = image distance (m) — positive for real image
    u = object distance (m) — negative (sign convention: object on left)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/lens_formulae.py
"""


def focal_length(object_distance: float, image_distance: float) -> float:
    """
    Calculate focal length from object and image distances.

    Using: 1/f = 1/v - 1/u  =>  f = (u * v) / (u - v)

    >>> round(focal_length(-20, 30), 4)
    12.0
    >>> round(focal_length(-10, 20), 4)
    6.6667
    >>> focal_length(0, 10)
    Traceback (most recent call last):
        ...
    ValueError: object_distance must not be zero
    >>> focal_length(10, 0)
    Traceback (most recent call last):
        ...
    ValueError: image_distance must not be zero
    """
    if object_distance == 0:
        raise ValueError("object_distance must not be zero")
    if image_distance == 0:
        raise ValueError("image_distance must not be zero")

    return (object_distance * image_distance) / (object_distance - image_distance)


def image_distance(focal_len: float, object_distance: float) -> float:
    """
    Calculate image distance from focal length and object distance.

    1/v = 1/f + 1/u  =>  v = (f * u) / (u - f)

    >>> round(image_distance(-12, -20), 4)
    -30.0
    >>> image_distance(0, -10)
    Traceback (most recent call last):
        ...
    ValueError: focal_length must not be zero
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
    Calculate object distance from focal length and image distance.

    1/u = 1/v - 1/f  =>  u = (f * v) / (f - v)

    >>> round(object_distance(-12, 30), 4)
    8.5714
    """
    if focal_len == 0:
        raise ValueError("focal_length must not be zero")
    if image_dist == 0:
        raise ValueError("image_distance must not be zero")
    if focal_len == image_dist:
        raise ValueError("image at focal point implies object at infinity")

    return (focal_len * image_dist) / (focal_len - image_dist)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
