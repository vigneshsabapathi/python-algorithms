"""
Lambert's Ellipsoidal Distance — distance on an ellipsoidal Earth model.

Lambert's formula calculates the shortest distance along the surface of an
oblate ellipsoid (the WGS84 Earth model) between two points. It provides
accuracy on the order of 10 metres over thousands of kilometres — much better
than the spherical Haversine for long ranges.

The algorithm:
    1. Convert geodetic latitudes to parametric (reduced) latitudes
    2. Compute central angle sigma via Haversine
    3. Compute correction terms P, Q, X, Y using parametric latitudes
    4. Apply Lambert's correction: d = a * (sigma - f/2 * (X + Y))

Reference:
    https://en.wikipedia.org/wiki/Geographical_distance#Lambert's_formula_for_long_lines

Run:
    python -m doctest geodesy/lamberts_ellipsoidal_distance.py -v
    python geodesy/lamberts_ellipsoidal_distance.py
"""

from math import atan, cos, radians, sin, tan

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from geodesy.haversine_distance import haversine_distance

AXIS_A = 6378137.0
AXIS_B = 6356752.314245
EQUATORIAL_RADIUS = 6378137


def lamberts_ellipsoidal_distance(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Calculate the shortest distance along an ellipsoidal Earth between two
    points given their latitude and longitude in degrees.

    Args:
        lat1, lon1: latitude and longitude of point 1 (degrees)
        lat2, lon2: latitude and longitude of point 2 (degrees)

    Returns:
        Distance in metres.

    Raises:
        ValueError: if latitude not in [-90, 90] or longitude not in [-180, 180]

    >>> lamberts_ellipsoidal_distance(100, 0, 0, 0)
    Traceback (most recent call last):
        ...
    ValueError: Latitude must be between -90 and 90 degrees

    >>> lamberts_ellipsoidal_distance(0, 0, -100, 0)
    Traceback (most recent call last):
        ...
    ValueError: Latitude must be between -90 and 90 degrees

    >>> lamberts_ellipsoidal_distance(0, 200, 0, 0)
    Traceback (most recent call last):
        ...
    ValueError: Longitude must be between -180 and 180 degrees

    >>> lamberts_ellipsoidal_distance(0, 0, 0, -200)
    Traceback (most recent call last):
        ...
    ValueError: Longitude must be between -180 and 180 degrees

    >>> from collections import namedtuple
    >>> point_2d = namedtuple("point_2d", "lat lon")
    >>> SAN_FRANCISCO = point_2d(37.774856, -122.424227)
    >>> YOSEMITE = point_2d(37.864742, -119.537521)
    >>> NEW_YORK = point_2d(40.713019, -74.012647)
    >>> VENICE = point_2d(45.443012, 12.313071)
    >>> f"{lamberts_ellipsoidal_distance(*SAN_FRANCISCO, *YOSEMITE):0,.0f} meters"
    '254,351 meters'
    >>> f"{lamberts_ellipsoidal_distance(*SAN_FRANCISCO, *NEW_YORK):0,.0f} meters"
    '4,138,992 meters'
    >>> f"{lamberts_ellipsoidal_distance(*SAN_FRANCISCO, *VENICE):0,.0f} meters"
    '9,737,326 meters'

    >>> # Same point — distance should be zero
    >>> lamberts_ellipsoidal_distance(0, 0, 0, 0)
    0.0
    """
    # Validate inputs
    if not -90 <= lat1 <= 90 or not -90 <= lat2 <= 90:
        raise ValueError("Latitude must be between -90 and 90 degrees")
    if not -180 <= lon1 <= 180 or not -180 <= lon2 <= 180:
        raise ValueError("Longitude must be between -180 and 180 degrees")

    # WGS84 flattening
    flattening = (AXIS_A - AXIS_B) / AXIS_A

    # Parametric (reduced) latitudes
    b_lat1 = atan((1 - flattening) * tan(radians(lat1)))
    b_lat2 = atan((1 - flattening) * tan(radians(lat2)))

    # Central angle via Haversine: sigma = haversine_distance / equatorial_radius
    sigma = haversine_distance(lat1, lon1, lat2, lon2) / EQUATORIAL_RADIUS

    # Same point — avoid division by zero in Y term (sin^2(sigma/2) == 0)
    if sigma == 0:
        return 0.0

    # Intermediate P and Q values
    p_value = (b_lat1 + b_lat2) / 2
    q_value = (b_lat2 - b_lat1) / 2

    # X = (sigma - sin(sigma)) * sin^2(P) * cos^2(Q) / cos^2(sigma/2)
    x_numerator = (sin(p_value) ** 2) * (cos(q_value) ** 2)
    x_denominator = cos(sigma / 2) ** 2
    x_value = (sigma - sin(sigma)) * (x_numerator / x_denominator)

    # Y = (sigma + sin(sigma)) * cos^2(P) * sin^2(Q) / sin^2(sigma/2)
    y_numerator = (cos(p_value) ** 2) * (sin(q_value) ** 2)
    y_denominator = sin(sigma / 2) ** 2
    y_value = (sigma + sin(sigma)) * (y_numerator / y_denominator)

    return EQUATORIAL_RADIUS * (sigma - ((flattening / 2) * (x_value + y_value)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    from collections import namedtuple

    point_2d = namedtuple("point_2d", "lat lon")
    SAN_FRANCISCO = point_2d(37.774856, -122.424227)
    YOSEMITE = point_2d(37.864742, -119.537521)
    NEW_YORK = point_2d(40.713019, -74.012647)
    VENICE = point_2d(45.443012, 12.313071)
    LONDON = point_2d(51.5074, -0.1278)
    TOKYO = point_2d(35.6762, 139.6503)

    pairs = [
        ("SF -> Yosemite", SAN_FRANCISCO, YOSEMITE),
        ("SF -> New York", SAN_FRANCISCO, NEW_YORK),
        ("SF -> Venice", SAN_FRANCISCO, VENICE),
        ("London -> Tokyo", LONDON, TOKYO),
    ]

    for label, p1, p2 in pairs:
        d = lamberts_ellipsoidal_distance(*p1, *p2)
        print(f"  {label:30s}: {d:>14,.2f} m  ({d / 1000:>10,.2f} km)")
