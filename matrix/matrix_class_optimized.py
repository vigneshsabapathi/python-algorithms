#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix Class.

The reference provides a full OOP Matrix class with arithmetic operators,
determinant (cofactor expansion), inverse, etc. The cofactor expansion
determinant is O(n!) which is very slow for large matrices.

Three alternatives:
  LUMatrix          -- LU decomposition for O(n^3) determinant and solve
  SparseMatrix      -- Dictionary-based sparse matrix for large sparse data
  FastMatrix        -- Optimized dense matrix with Gauss elimination determinant

Run:
    python matrix/matrix_class_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.matrix_class import Matrix as ReferenceMatrix


# ---------------------------------------------------------------------------
# Variant 1 -- LU Decomposition Matrix
# ---------------------------------------------------------------------------

class LUMatrix:
    """
    Matrix with LU decomposition for efficient determinant and solving.

    >>> m = LUMatrix([[1, 2], [3, 4]])
    >>> m.determinant()
    -2.0
    >>> m = LUMatrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    >>> m.determinant()
    1.0
    >>> m = LUMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> abs(m.determinant()) < 1e-10
    True
    """

    def __init__(self, rows: list[list[float]]) -> None:
        self.rows = [row[:] for row in rows]
        self.n = len(rows)

    def determinant(self) -> float:
        """Compute determinant via Gaussian elimination. O(n^3)."""
        mat = [row[:] for row in self.rows]
        n = self.n
        sign = 1

        for col in range(n):
            # Partial pivoting
            max_row = max(range(col, n), key=lambda r: abs(mat[r][col]))
            if abs(mat[max_row][col]) < 1e-12:
                return 0.0
            if max_row != col:
                mat[col], mat[max_row] = mat[max_row], mat[col]
                sign *= -1

            for row in range(col + 1, n):
                factor = mat[row][col] / mat[col][col]
                for j in range(col, n):
                    mat[row][j] -= factor * mat[col][j]

        det = sign
        for i in range(n):
            det *= mat[i][i]
        return float(det)

    def __repr__(self) -> str:
        return f"LUMatrix({self.rows})"


# ---------------------------------------------------------------------------
# Variant 2 -- Sparse Matrix (dictionary of non-zero entries)
# ---------------------------------------------------------------------------

class SparseMatrix:
    """
    Sparse matrix using dictionary storage. Efficient for matrices with many zeros.

    >>> s = SparseMatrix(3, 3)
    >>> s[0, 0] = 1
    >>> s[1, 1] = 2
    >>> s[2, 2] = 3
    >>> s[0, 0]
    1
    >>> s[0, 1]
    0
    >>> s.nnz()
    3
    >>> s2 = SparseMatrix.from_dense([[1, 0], [0, 2]])
    >>> s2.to_dense()
    [[1, 0], [0, 2]]
    """

    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.data: dict[tuple[int, int], float] = {}

    def __setitem__(self, key: tuple[int, int], value: float) -> None:
        if value != 0:
            self.data[key] = value
        elif key in self.data:
            del self.data[key]

    def __getitem__(self, key: tuple[int, int]) -> float:
        return self.data.get(key, 0)

    def nnz(self) -> int:
        """Number of non-zero elements."""
        return len(self.data)

    def to_dense(self) -> list[list[float]]:
        result = [[0] * self.cols for _ in range(self.rows)]
        for (r, c), v in self.data.items():
            result[r][c] = v
        return result

    @classmethod
    def from_dense(cls, matrix: list[list[float]]) -> SparseMatrix:
        rows, cols = len(matrix), len(matrix[0]) if matrix else 0
        s = cls(rows, cols)
        for i, row in enumerate(matrix):
            for j, val in enumerate(row):
                if val != 0:
                    s[i, j] = val
        return s

    def multiply(self, other: SparseMatrix) -> SparseMatrix:
        """Sparse matrix multiplication. Only multiplies non-zero entries."""
        assert self.cols == other.rows
        result = SparseMatrix(self.rows, other.cols)
        # Group other's entries by row for efficient lookup
        other_by_row: dict[int, list[tuple[int, float]]] = {}
        for (r, c), v in other.data.items():
            other_by_row.setdefault(r, []).append((c, v))

        for (i, k), a_val in self.data.items():
            if k in other_by_row:
                for j, b_val in other_by_row[k]:
                    result[i, j] = result[i, j] + a_val * b_val
        return result


# ---------------------------------------------------------------------------
# Variant 3 -- Fast dense matrix with optimized operations
# ---------------------------------------------------------------------------

class FastMatrix:
    """
    Dense matrix with O(n^3) determinant via Gaussian elimination.

    >>> m = FastMatrix([[2, 1], [5, 3]])
    >>> round(m.determinant(), 10)
    1.0
    >>> m.transpose().rows
    [[2, 5], [1, 3]]
    >>> (m + m).rows
    [[4, 2], [10, 6]]
    >>> (m * 2).rows
    [[4, 2], [10, 6]]
    """

    def __init__(self, rows: list[list[float]]) -> None:
        self.rows = [row[:] for row in rows]

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.rows), len(self.rows[0]) if self.rows else 0

    def determinant(self) -> float:
        n = len(self.rows)
        mat = [row[:] for row in self.rows]
        sign = 1
        for col in range(n):
            max_row = max(range(col, n), key=lambda r: abs(mat[r][col]))
            if abs(mat[max_row][col]) < 1e-12:
                return 0.0
            if max_row != col:
                mat[col], mat[max_row] = mat[max_row], mat[col]
                sign *= -1
            for row in range(col + 1, n):
                factor = mat[row][col] / mat[col][col]
                for j in range(col, n):
                    mat[row][j] -= factor * mat[col][j]
        return float(sign * (1 if not mat else
                     eval("*".join(str(mat[i][i]) for i in range(n)))))

    def transpose(self) -> FastMatrix:
        return FastMatrix([list(col) for col in zip(*self.rows)])

    def __add__(self, other: FastMatrix) -> FastMatrix:
        return FastMatrix([
            [a + b for a, b in zip(r1, r2)]
            for r1, r2 in zip(self.rows, other.rows)
        ])

    def __mul__(self, scalar: float) -> FastMatrix:
        return FastMatrix([[x * scalar for x in row] for row in self.rows])

    def __repr__(self) -> str:
        return f"FastMatrix({self.rows})"


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    data = [[2, 1, 3], [5, 3, 7], [1, 4, 2]]
    number = 10_000
    print(f"Benchmark ({number} determinant computations on 3x3):\n")

    funcs = [
        ("ReferenceMatrix (cofactor O(n!))", lambda: ReferenceMatrix(data).determinant()),
        ("LUMatrix (Gaussian O(n^3))", lambda: LUMatrix(data).determinant()),
        ("FastMatrix (Gaussian O(n^3))", lambda: FastMatrix(data).determinant()),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:42s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
