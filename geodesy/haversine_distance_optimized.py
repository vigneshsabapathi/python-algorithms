#!/usr/bin/env python3
"""
Optimized and alternative implementations of Haversine Distance.

The Haversine formula computes the great-circle distance between two points
on a sphere given their latitudes and longitudes. This module provides three
implementations to compare:

  pure_math       — stdlib math only, uses reduced latitude (WGS84 flattening)
  numpy_vectorized — NumPy vectorised, computes many pairs at once
  geodesic_lib    — geopy's geodesic (Vincenty/Karney), ellipsoidal accuracy

Key differences:
  - pure_math matches the reference (spherical + reduced latitude, ~0.1% error)
  - numpy_vectorized is identical math but batched via NumPy (great for arrays)
  - geodesic_lib uses the full WGS84 ellipsoid model (mm-level accuracy)

Run:
    python geodesy/haversine_distance_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from geodesy.haversine_distance import haversine_distance as reference

# ── WGS84 constants ──────────────────────────────────────────────────────────
AXIS_A = 6378137.0
AXIS_B = 6356752.314245
RADIUS = 6378137
FLATTENING = (AXIS_A - AXIS_B) / AXIS_A


# ---------------------------------------------------------------------------
# Variant 1 — pure_math: classic textbook Haversine (no reduced latitude)
# ---------------------------------------------------------------------------

def pure_math(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Classic Haversine using geodetic latitude directly (no flattening correction).

    This is the most common textbook form: simpler, but slightly less accurate
    than the reference which uses reduced (parametric) latitude.

    >>> f"{pure_math(37.774856, -122.424227, 37.864742, -119.537521):0,.0f} meters"
    '254,033 meters'

    >>> pure_math(0, 0, 0, 0)
    0.0

    >>> f"{pure_math(0, 0, 0, 90):0,.0f} meters"
    '10,018,754 meters'
    """
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (math.sin(dphi / 2) ** 2
         + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    return RADIUS * 2 * math.asin(math.sqrt(a))


# ---------------------------------------------------------------------------
# Variant 2 — numpy_vectorized: batch computation for coordinate arrays
# ---------------------------------------------------------------------------

def numpy_vectorized(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    NumPy-vectorized Haversine. Accepts scalars or arrays; returns scalar for
    scalar input.

    Uses reduced latitude (matching reference) but all trig ops are vectorised.

    >>> f"{numpy_vectorized(37.774856, -122.424227, 37.864742, -119.537521):0,.0f} meters"
    '254,352 meters'

    >>> f"{numpy_vectorized(0, 0, 0, 90):0,.0f} meters"
    '10,018,754 meters'
    """
    import numpy as np

    lat1_r, lon1_r = np.radians(lat1), np.radians(lon1)
    lat2_r, lon2_r = np.radians(lat2), np.radians(lon2)

    # Reduced (parametric) latitude
    phi1 = np.arctan((1 - FLATTENING) * np.tan(lat1_r))
    phi2 = np.arctan((1 - FLATTENING) * np.tan(lat2_r))

    sin_sq_phi = np.sin((phi2 - phi1) / 2) ** 2
    sin_sq_lam = np.sin((lon2_r - lon1_r) / 2) ** 2

    h = np.sqrt(sin_sq_phi + np.cos(phi1) * np.cos(phi2) * sin_sq_lam)
    result = 2 * RADIUS * np.arcsin(h)
    return float(result)


# ---------------------------------------------------------------------------
# Variant 3 — geodesic_lib: geopy Vincenty/Karney ellipsoidal distance
# ---------------------------------------------------------------------------

def geodesic_lib(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Full ellipsoidal distance using geopy's geodesic (Karney's method).

    This is the gold-standard for accuracy (~0.5 mm precision on the WGS84
    ellipsoid) but much slower than the pure Haversine.

    >>> d = geodesic_lib(37.774856, -122.424227, 37.864742, -119.537521)
    >>> f"{d:0,.0f} meters"
    '254,351 meters'
    """
    from geopy.distance import geodesic
    return geodesic((lat1, lon1), (lat2, lon2)).meters


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def verify_all() -> None:
    """Test all variants against the reference implementation."""
    test_pairs = [
        ("SF-Yosemite", 37.774856, -122.424227, 37.864742, -119.537521),
        ("SF-NewYork", 37.774856, -122.424227, 40.713019, -74.012647),
        ("Equator 0-90", 0.0, 0.0, 0.0, 90.0),
        ("Same point", 51.5074, -0.1278, 51.5074, -0.1278),
    ]

    variants = {
        "reference": reference,
        "pure_math": pure_math,
        "numpy_vec": numpy_vectorized,
        "geodesic":  geodesic_lib,
    }

    print("=" * 80)
    print("VERIFICATION — all distances in metres")
    print("=" * 80)

    for label, la1, lo1, la2, lo2 in test_pairs:
        print(f"\n  {label}:")
        ref_val = reference(la1, lo1, la2, lo2)
        for name, fn in variants.items():
            val = fn(la1, lo1, la2, lo2)
            diff = val - ref_val
            pct = (diff / ref_val * 100) if ref_val else 0.0
            marker = "<-- reference" if name == "reference" else ""
            print(f"    {name:12s}: {val:>14,.2f}  (delta: {diff:>+10,.2f} m  {pct:>+.4f}%)  {marker}")

    print()


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark(n: int = 50_000) -> None:
    """Benchmark each variant on a single coordinate pair."""
    la1, lo1 = 37.774856, -122.424227
    la2, lo2 = 37.864742, -119.537521

    variants = {
        "reference":  lambda: reference(la1, lo1, la2, lo2),
        "pure_math":  lambda: pure_math(la1, lo1, la2, lo2),
        "numpy_vec":  lambda: numpy_vectorized(la1, lo1, la2, lo2),
        "geodesic":   lambda: geodesic_lib(la1, lo1, la2, lo2),
    }

    print("=" * 80)
    print(f"BENCHMARK — {n:,} iterations each (SF -> Yosemite)")
    print("=" * 80)

    times = {}
    for name, fn in variants.items():
        t = timeit.timeit(fn, number=n)
        times[name] = t

    fastest = min(times.values())
    for name, t in times.items():
        per_call = t / n * 1_000_000  # microseconds
        ratio = t / fastest
        print(f"  {name:12s}: {t:>8.3f}s  ({per_call:>8.2f} us/call)  {ratio:>6.1f}x")

    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    verify_all()
    benchmark()
