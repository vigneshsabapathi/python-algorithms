"""

Task:
Implement the Sherman-Morrison formula for efficiently updating a matrix
inverse when a rank-1 update is applied.

Formula: (A + uv^T)^(-1) = A^(-1) - (A^(-1) u v^T A^(-1)) / (1 + v^T A^(-1) u)

Implementation notes: Includes a full Matrix class with arithmetic operators,
transpose, and the Sherman-Morrison method. O(n^2) for the update instead of
O(n^3) for recomputing the full inverse.

Reference: https://en.wikipedia.org/wiki/Sherman%E2%80%93Morrison_formula
Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/sherman_morrison.py
"""

from __future__ import annotations

from typing import Any


class Matrix:
    """
    Matrix class with Sherman-Morrison formula implementation.

    >>> a = Matrix(2, 3, 1)
    >>> a
    Matrix consist of 2 rows and 3 columns
    [1, 1, 1]
    [1, 1, 1]
    >>> a[0, 0]
    1
    """

    def __init__(self, row: int, column: int, default_value: float = 0) -> None:
        self.row, self.column = row, column
        self.array = [[default_value for _ in range(column)] for _ in range(row)]

    def __str__(self) -> str:
        s = f"Matrix consist of {self.row} rows and {self.column} columns\n"
        max_len = 0
        for row_vector in self.array:
            for obj in row_vector:
                max_len = max(max_len, len(str(obj)))
        fmt = f"%{max_len}s"

        def single_line(row_vector: list[float]) -> str:
            return "[" + ", ".join(fmt % (obj,) for obj in row_vector) + "]"

        s += "\n".join(single_line(row_vector) for row_vector in self.array)
        return s

    def __repr__(self) -> str:
        return str(self)

    def validate_indices(self, loc: tuple[int, int]) -> bool:
        """
        >>> a = Matrix(2, 6, 0)
        >>> a.validate_indices((2, 7))
        False
        >>> a.validate_indices((0, 0))
        True
        """
        if not (isinstance(loc, (list, tuple)) and len(loc) == 2):
            return False
        elif not (0 <= loc[0] < self.row and 0 <= loc[1] < self.column):
            return False
        return True

    def __getitem__(self, loc: tuple[int, int]) -> Any:
        """
        >>> a = Matrix(3, 2, 7)
        >>> a[1, 0]
        7
        """
        assert self.validate_indices(loc)
        return self.array[loc[0]][loc[1]]

    def __setitem__(self, loc: tuple[int, int], value: float) -> None:
        """
        >>> a = Matrix(2, 3, 1)
        >>> a[1, 2] = 51
        >>> a[1, 2]
        51
        """
        assert self.validate_indices(loc)
        self.array[loc[0]][loc[1]] = value

    def __add__(self, another: Matrix) -> Matrix:
        """
        >>> a = Matrix(2, 1, -4)
        >>> b = Matrix(2, 1, 3)
        >>> c = a + b
        >>> c[0, 0]
        -1
        """
        assert isinstance(another, Matrix)
        assert self.row == another.row and self.column == another.column
        result = Matrix(self.row, self.column)
        for r in range(self.row):
            for c in range(self.column):
                result[r, c] = self[r, c] + another[r, c]
        return result

    def __neg__(self) -> Matrix:
        """
        >>> a = Matrix(2, 2, 3)
        >>> b = -a
        >>> b[0, 0]
        -3
        """
        result = Matrix(self.row, self.column)
        for r in range(self.row):
            for c in range(self.column):
                result[r, c] = -self[r, c]
        return result

    def __sub__(self, another: Matrix) -> Matrix:
        return self + (-another)

    def __mul__(self, another: float | Matrix) -> Matrix:
        """
        >>> a = Matrix(2, 3, 1)
        >>> a[0, 2] = a[1, 2] = 3
        >>> b = a * -2
        >>> b[0, 2]
        -6
        """
        if isinstance(another, (int, float)):
            result = Matrix(self.row, self.column)
            for r in range(self.row):
                for c in range(self.column):
                    result[r, c] = self[r, c] * another
            return result
        elif isinstance(another, Matrix):
            assert self.column == another.row
            result = Matrix(self.row, another.column)
            for r in range(self.row):
                for c in range(another.column):
                    for i in range(self.column):
                        result[r, c] += self[r, i] * another[i, c]
            return result
        else:
            raise TypeError(f"Unsupported type given for another ({type(another)})")

    def transpose(self) -> Matrix:
        """
        >>> a = Matrix(2, 3)
        >>> for r in range(2):
        ...     for c in range(3):
        ...         a[r, c] = r * c
        >>> t = a.transpose()
        >>> t[2, 1]
        2
        """
        result = Matrix(self.column, self.row)
        for r in range(self.row):
            for c in range(self.column):
                result[c, r] = self[r, c]
        return result

    def sherman_morrison(self, u: Matrix, v: Matrix) -> Any:
        """
        Apply Sherman-Morrison formula: (A + uv^T)^(-1) where A^(-1) is self.
        Returns None if the denominator is zero.

        >>> ainv = Matrix(3, 3, 0)
        >>> for i in range(3): ainv[i, i] = 1
        >>> u = Matrix(3, 1, 0)
        >>> u[0, 0], u[1, 0], u[2, 0] = 1, 2, -3
        >>> v = Matrix(3, 1, 0)
        >>> v[0, 0], v[1, 0], v[2, 0] = 4, -2, 5
        >>> result = ainv.sherman_morrison(u, v)
        >>> round(result[0, 0], 4)
        1.2857
        """
        assert isinstance(u, Matrix) and isinstance(v, Matrix)
        assert self.row == self.column == u.row == v.row
        assert u.column == v.column == 1

        v_t = v.transpose()
        numerator_factor = (v_t * self * u)[0, 0] + 1
        if numerator_factor == 0:
            return None
        return self - ((self * u) * (v_t * self) * (1.0 / numerator_factor))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
