"""
Koch Snowflake — Iterative Fractal Curve Construction

The Koch snowflake is built by starting with an equilateral triangle and
repeatedly replacing each line segment's middle third with an outward-pointing
equilateral bump.  After n iterations the curve has 3 * 4^n segments.

Reference: https://en.wikipedia.org/wiki/Koch_snowflake
Based on: https://github.com/TheAlgorithms/Python/blob/master/fractals/koch_snowflake.py
"""

from __future__ import annotations

import numpy as np

# Initial equilateral triangle (closed loop)
VECTOR_1 = np.array([0.0, 0.0])
VECTOR_2 = np.array([0.5, 0.8660254])
VECTOR_3 = np.array([1.0, 0.0])
INITIAL_VECTORS = [VECTOR_1, VECTOR_2, VECTOR_3, VECTOR_1]


def rotate(vector: np.ndarray, angle_in_degrees: float) -> np.ndarray:
    """
    Rotate a 2-D vector by *angle_in_degrees* counter-clockwise.

    >>> rotate(np.array([1, 0]), 60)
    array([0.5      , 0.8660254])
    >>> rotate(np.array([1, 0]), 90)
    array([6.123234e-17, 1.000000e+00])
    """
    theta = np.radians(angle_in_degrees)
    c, s = np.cos(theta), np.sin(theta)
    rotation_matrix = np.array(((c, -s), (s, c)))
    return np.dot(rotation_matrix, vector)


def iteration_step(vectors: list[np.ndarray]) -> list[np.ndarray]:
    """
    One Koch iteration: replace each segment with four sub-segments
    (two straight thirds + one 60-degree bump).

    >>> iteration_step([np.array([0, 0]), np.array([1, 0])])
    [array([0, 0]), array([0.33333333, 0.        ]), array([0.5       , 0.28867513]), array([0.66666667, 0.        ]), array([1, 0])]
    """
    new_vectors: list[np.ndarray] = []
    for i, start_vector in enumerate(vectors[:-1]):
        end_vector = vectors[i + 1]
        diff = end_vector - start_vector
        new_vectors.append(start_vector)
        new_vectors.append(start_vector + diff / 3)
        new_vectors.append(start_vector + diff / 3 + rotate(diff / 3, 60))
        new_vectors.append(start_vector + diff * 2 / 3)
    new_vectors.append(vectors[-1])
    return new_vectors


def iterate(initial_vectors: list[np.ndarray], steps: int) -> list[np.ndarray]:
    """
    Apply *steps* Koch iterations to *initial_vectors*.

    >>> iterate([np.array([0, 0]), np.array([1, 0])], 1)
    [array([0, 0]), array([0.33333333, 0.        ]), array([0.5       , 0.28867513]), array([0.66666667, 0.        ]), array([1, 0])]
    >>> len(iterate([np.array([0, 0]), np.array([1, 0])], 0))
    2
    >>> len(iterate([np.array([0, 0]), np.array([1, 0])], 2))
    17
    """
    vectors = initial_vectors
    for _ in range(steps):
        vectors = iteration_step(vectors)
    return vectors


def snowflake_vertices(steps: int) -> int:
    """
    Return the number of vertices in a Koch snowflake after *steps* iterations.
    Formula: 3 * 4^steps + 1 (closed polygon).

    >>> snowflake_vertices(0)
    4
    >>> snowflake_vertices(1)
    13
    >>> snowflake_vertices(2)
    49
    """
    return 3 * (4 ** steps) + 1


def snowflake_perimeter(side_length: float, steps: int) -> float:
    """
    Perimeter after *steps* iterations for an initial triangle with *side_length*.
    Each iteration multiplies by 4/3.

    >>> round(snowflake_perimeter(1.0, 0), 4)
    3.0
    >>> round(snowflake_perimeter(1.0, 1), 4)
    4.0
    >>> round(snowflake_perimeter(1.0, 5), 4)
    12.642
    """
    return 3 * side_length * (4 / 3) ** steps


def snowflake_area(side_length: float, steps: int) -> float:
    """
    Area of a Koch snowflake after *steps* iterations.
    Converges to (2 * sqrt(3) / 5) * s^2.

    >>> round(snowflake_area(1.0, 0), 6)
    0.433013
    >>> round(snowflake_area(1.0, 1), 6)
    0.57735
    >>> round(snowflake_area(1.0, 10), 6)
    0.692742
    """
    # Area of initial equilateral triangle
    a0 = (np.sqrt(3) / 4) * side_length ** 2
    area = a0
    for k in range(1, steps + 1):
        # At step k we add 3 * 4^(k-1) triangles each with side s/3^k
        num_new = 3 * 4 ** (k - 1)
        new_side = side_length / 3 ** k
        area += num_new * (np.sqrt(3) / 4) * new_side ** 2
    return float(area)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("=== Koch Snowflake Demo ===")
    for s in range(6):
        verts = iterate(INITIAL_VECTORS, s)
        perim = snowflake_perimeter(1.0, s)
        area = snowflake_area(1.0, s)
        print(
            f"Step {s}: {len(verts):>5} vertices, "
            f"perimeter = {perim:.4f}, area = {area:.6f}"
        )
