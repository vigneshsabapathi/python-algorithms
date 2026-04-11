"""
Haversine Distance — great-circle distance between two GPS coordinates.

The Haversine formula calculates the shortest distance over the Earth's surface
between two points given their latitude and longitude. It models the Earth as a
sphere, which introduces ~0.3% error vs ellipsoidal methods but is fast and
sufficient for most applications.

Formula:
    a = sin^2((phi2 - phi1)/2) + cos(phi1) * cos(phi2) * sin^2((lam2 - lam1)/2)
    c = 2 * asin(sqrt(a))
    d = R * c

where phi = reduced latitude, lam = longitude in radians, R = Earth radius.

WGS84 constants:
    Semi-major axis (a) = 6,378,137.0 m
    Semi-minor axis (b) = 6,356,752.314245 m

Reference: https://en.wikipedia.org/wiki/Haversine_formula

Run:
    python -m doctest geodesy/haversine_distance.py -v
    python geodesy/haversine_distance.py
"""

from math import asin, atan, cos, radians, sin, sqrt, tan

AXIS_A = 6378137.0
AXIS_B = 6356752.314245
RADIUS = 6378137


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great-circle distance between two points on a sphere,
    given longitudes and latitudes in degrees.

    Uses reduced (parametric) latitude for slightly better accuracy on the
    WGS84 ellipsoid, though this is still fundamentally a spherical formula.

    Args:
        lat1, lon1: latitude and longitude of point 1 (degrees)
        lat2, lon2: latitude and longitude of point 2 (degrees)

    Returns:
        Distance in metres.

    >>> from collections import namedtuple
    >>> point_2d = namedtuple("point_2d", "lat lon")
    >>> SAN_FRANCISCO = point_2d(37.774856, -122.424227)
    >>> YOSEMITE = point_2d(37.864742, -119.537521)
    >>> f"{haversine_distance(*SAN_FRANCISCO, *YOSEMITE):0,.0f} meters"
    '254,352 meters'

    >>> # Same point — distance should be zero
    >>> haversine_distance(0, 0, 0, 0)
    0.0

    >>> # Antipodal points (poles) — half circumference
    >>> f"{haversine_distance(90, 0, -90, 0):0,.0f} meters"
    '20,037,508 meters'

    >>> # Equator quarter arc (0,0) to (0,90)
    >>> f"{haversine_distance(0, 0, 0, 90):0,.0f} meters"
    '10,018,754 meters'
    """
    # WGS84 flattening — converts geodetic latitude to reduced (parametric) latitude
    flattening = (AXIS_A - AXIS_B) / AXIS_A
    phi_1 = atan((1 - flattening) * tan(radians(lat1)))
    phi_2 = atan((1 - flattening) * tan(radians(lat2)))
    lambda_1 = radians(lon1)
    lambda_2 = radians(lon2)

    # Haversine formula components
    sin_sq_phi = sin((phi_2 - phi_1) / 2)
    sin_sq_lambda = sin((lambda_2 - lambda_1) / 2)
    sin_sq_phi *= sin_sq_phi
    sin_sq_lambda *= sin_sq_lambda

    h_value = sqrt(sin_sq_phi + (cos(phi_1) * cos(phi_2) * sin_sq_lambda))
    return 2 * RADIUS * asin(h_value)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    from collections import namedtuple

    point_2d = namedtuple("point_2d", "lat lon")
    SAN_FRANCISCO = point_2d(37.774856, -122.424227)
    YOSEMITE = point_2d(37.864742, -119.537521)
    NEW_YORK = point_2d(40.713019, -74.012647)
    VENICE = point_2d(45.443012, 12.313071)

    pairs = [
        ("SF -> Yosemite", SAN_FRANCISCO, YOSEMITE),
        ("SF -> New York", SAN_FRANCISCO, NEW_YORK),
        ("SF -> Venice", SAN_FRANCISCO, VENICE),
        ("North Pole -> South Pole", point_2d(90, 0), point_2d(-90, 0)),
    ]

    for label, p1, p2 in pairs:
        d = haversine_distance(*p1, *p2)
        print(f"  {label:30s}: {d:>14,.2f} m  ({d / 1000:>10,.2f} km)")
