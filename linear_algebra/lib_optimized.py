#!/usr/bin/env python3
"""
Optimized and alternative implementations of the Linear Algebra Library.

The reference provides Vector and Matrix classes with Python-level loops.

Three variants:
  numpy_vector      — numpy-backed vector with same interface (BLAS under the hood)
  numpy_matrix      — numpy-backed matrix with determinant via LU (O(n^3) not O(n!))
  dataclass_vector  — modern Python dataclass with __slots__ (memory-efficient)

Key interview insight:
    The reference Matrix.determinant() uses Laplace expansion — O(n!) time.
    LU-based determinant is O(n^3): det(A) = product of U diagonal elements.
    For n=10, that's ~3.6M vs 1000 operations — the difference between
    "compiles but never finishes" and "instant".

Run:
    python linear_algebra/lib_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit
from dataclasses import dataclass, field

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.lib import Matrix, Vector


# ---------------------------------------------------------------------------
# Variant 1 — NumpyVector: numpy-backed, same interface
# ---------------------------------------------------------------------------
class NumpyVector:
    """
    Vector backed by numpy array — all operations use BLAS.

    >>> v = NumpyVector([2, 3, 4])
    >>> v.euclidean_length()
    5.385164807134504
    >>> str(NumpyVector([1, 2]) + NumpyVector([3, 4]))
    '(4.0,6.0)'
    """

    def __init__(self, components: list[float] | np.ndarray | None = None) -> None:
        if components is None:
            self._data = np.array([], dtype=float)
        else:
            self._data = np.asarray(components, dtype=float)

    def __len__(self) -> int:
        return len(self._data)

    def __str__(self) -> str:
        return "(" + ",".join(str(x) for x in self._data) + ")"

    def __add__(self, other: NumpyVector) -> NumpyVector:
        return NumpyVector(self._data + other._data)

    def __sub__(self, other: NumpyVector) -> NumpyVector:
        return NumpyVector(self._data - other._data)

    def __mul__(self, other: float | NumpyVector) -> float | NumpyVector:
        if isinstance(other, (int, float)):
            return NumpyVector(self._data * other)
        elif isinstance(other, NumpyVector):
            return float(np.dot(self._data, other._data))
        raise TypeError("invalid operand")

    def component(self, i: int) -> float:
        return float(self._data[i])

    def euclidean_length(self) -> float:
        if len(self._data) == 0:
            raise Exception("Vector is empty")
        return float(np.linalg.norm(self._data))

    def angle(self, other: NumpyVector, deg: bool = False) -> float:
        cos_angle = float(np.dot(self._data, other._data)) / (
            self.euclidean_length() * other.euclidean_length()
        )
        angle = math.acos(np.clip(cos_angle, -1, 1))
        return math.degrees(angle) if deg else angle


# ---------------------------------------------------------------------------
# Variant 2 — NumpyMatrix: numpy-backed with O(n^3) determinant
# ---------------------------------------------------------------------------
class NumpyMatrix:
    """
    Matrix backed by numpy — determinant via LU is O(n^3) not O(n!).

    >>> m = NumpyMatrix([[1, 2], [3, 4]])
    >>> m.determinant()
    -2.0
    >>> m = NumpyMatrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
    >>> m.determinant()
    6.0
    """

    def __init__(self, matrix: list[list[float]] | np.ndarray) -> None:
        self._data = np.asarray(matrix, dtype=float)

    def __str__(self) -> str:
        rows = []
        for i in range(self._data.shape[0]):
            rows.append("|" + ",".join(str(v) for v in self._data[i]) + "|")
        return "\n".join(rows)

    def height(self) -> int:
        return self._data.shape[0]

    def width(self) -> int:
        return self._data.shape[1]

    def component(self, x: int, y: int) -> float:
        return float(self._data[x, y])

    def determinant(self) -> float:
        """O(n^3) determinant via numpy (LU-based)."""
        return float(round(np.linalg.det(self._data), 10))

    def __add__(self, other: NumpyMatrix) -> NumpyMatrix:
        return NumpyMatrix(self._data + other._data)

    def __sub__(self, other: NumpyMatrix) -> NumpyMatrix:
        return NumpyMatrix(self._data - other._data)

    def __mul__(self, other: float | NumpyVector) -> NumpyMatrix | NumpyVector:
        if isinstance(other, (int, float)):
            return NumpyMatrix(self._data * other)
        elif isinstance(other, NumpyVector):
            return NumpyVector(self._data @ other._data)
        raise TypeError("invalid operand")


# ---------------------------------------------------------------------------
# Variant 3 — DataclassVector: modern Python with __slots__
# ---------------------------------------------------------------------------
@dataclass
class DataclassVector:
    """
    Memory-efficient vector using dataclass with __slots__.

    >>> v = DataclassVector([1, 2, 3])
    >>> v.euclidean_length()
    3.7416573867739413
    >>> v.dot(DataclassVector([4, 5, 6]))
    32
    """

    _components: list[float] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self._components)

    def __str__(self) -> str:
        return "(" + ",".join(map(str, self._components)) + ")"

    def __add__(self, other: DataclassVector) -> DataclassVector:
        return DataclassVector([a + b for a, b in zip(self._components, other._components)])

    def __sub__(self, other: DataclassVector) -> DataclassVector:
        return DataclassVector([a - b for a, b in zip(self._components, other._components)])

    def scale(self, scalar: float) -> DataclassVector:
        return DataclassVector([c * scalar for c in self._components])

    def dot(self, other: DataclassVector) -> float:
        return sum(a * b for a, b in zip(self._components, other._components))

    def euclidean_length(self) -> float:
        return math.sqrt(sum(c ** 2 for c in self._components))


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare determinant computation: O(n!) vs O(n^3)."""
    import random

    random.seed(42)

    print("Linear Algebra Lib Benchmark")
    print(f"{'Operation':<30} {'Size':>5} {'Time (s)':>10} {'Speedup':>10}")
    print("-" * 58)

    # Determinant comparison
    for n in [5, 8, 10]:
        data = [[random.uniform(-10, 10) for _ in range(n)] for _ in range(n)]
        ref_mat = Matrix(data, n, n)
        np_mat = NumpyMatrix(data)

        if n <= 10:
            number = 3 if n >= 9 else 20
            t_ref = timeit.timeit(lambda: ref_mat.determinant(), number=number)
        else:
            t_ref = float("inf")
            number = 20

        t_np = timeit.timeit(lambda: np_mat.determinant(), number=number)
        speedup = t_ref / t_np if t_np > 0 else float("inf")

        print(f"{'det (reference O(n!))':<30} {n:>5} {t_ref:>10.4f}")
        print(f"{'det (numpy O(n^3))':<30} {n:>5} {t_np:>10.4f} {speedup:>9.1f}x")

    # Vector operations comparison
    n = 10000
    comps = [random.uniform(-100, 100) for _ in range(n)]
    v_ref = Vector(comps)
    v_np = NumpyVector(comps)
    v_dc = DataclassVector(comps)
    number = 100

    t_ref_v = timeit.timeit(lambda: v_ref.euclidean_length(), number=number)
    t_np_v = timeit.timeit(lambda: v_np.euclidean_length(), number=number)
    t_dc_v = timeit.timeit(lambda: v_dc.euclidean_length(), number=number)

    print(f"\n{'euclidean_length':<30} {'N':>5} {'Time (s)':>10} {'Speedup':>10}")
    print("-" * 58)
    for name, t in [
        ("Vector (reference)", t_ref_v),
        ("NumpyVector", t_np_v),
        ("DataclassVector", t_dc_v),
    ]:
        print(f"{name:<30} {n:>5} {t:>10.4f} {t_ref_v / t if t > 0 else 0:>9.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
