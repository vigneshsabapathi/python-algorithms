"""

Task:
OOP implementation of a Matrix class with common operations:
arithmetic (+, -, *, **), determinant, inverse, cofactors,
minors, adjugate, identity, transpose.

Implementation notes: Stores rows as list of lists. Supports int/float
elements. Scalar and matrix multiplication via __mul__. Power via
repeated multiplication. Inverse via adjugate/determinant.

Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/matrix_class.py
"""

from __future__ import annotations


class Matrix:
    """
    Matrix object with arithmetic operations.

    >>> m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> m.order
    (3, 3)
    >>> m.is_square
    True
    >>> m.determinant()
    0
    >>> m.is_invertable()
    False
    >>> print(Matrix([[1, 2], [3, 4]]).determinant())
    -2
    >>> print(-Matrix([[1, 2], [3, 4]]))
    [[-1. -2.]
     [-3. -4.]]
    >>> print(Matrix([[1, 2], [3, 4]]) * 2)
    [[2. 4.]
     [6. 8.]]
    >>> print(Matrix([[1, 2], [3, 4]]) + Matrix([[5, 6], [7, 8]]))
    [[6. 8.]
     [10. 12.]]
    >>> print(Matrix([[1, 2], [3, 4]]) ** 2)
    [[7. 10.]
     [15. 22.]]
    """

    def __init__(self, rows: list[list[int]]):
        error = TypeError(
            "Matrices must be formed from a list of zero or more lists containing at "
            "least one and the same number of values, each of which must be of type "
            "int or float."
        )
        if len(rows) != 0:
            cols = len(rows[0])
            if cols == 0:
                raise error
            for row in rows:
                if len(row) != cols:
                    raise error
                for value in row:
                    if not isinstance(value, (int, float)):
                        raise error
            self.rows = rows
        else:
            self.rows = []

    def columns(self) -> list[list[int]]:
        return [[row[i] for row in self.rows] for i in range(len(self.rows[0]))]

    @property
    def num_rows(self) -> int:
        return len(self.rows)

    @property
    def num_columns(self) -> int:
        return len(self.rows[0])

    @property
    def order(self) -> tuple[int, int]:
        return self.num_rows, self.num_columns

    @property
    def is_square(self) -> bool:
        return self.order[0] == self.order[1]

    def identity(self) -> Matrix:
        values = [
            [0 if column_num != row_num else 1 for column_num in range(self.num_rows)]
            for row_num in range(self.num_rows)
        ]
        return Matrix(values)

    def determinant(self) -> int:
        if not self.is_square:
            return 0
        if self.order == (0, 0):
            return 1
        if self.order == (1, 1):
            return int(self.rows[0][0])
        if self.order == (2, 2):
            return int(
                (self.rows[0][0] * self.rows[1][1])
                - (self.rows[0][1] * self.rows[1][0])
            )
        return sum(
            self.rows[0][column] * self.cofactors().rows[0][column]
            for column in range(self.num_columns)
        )

    def is_invertable(self) -> bool:
        return bool(self.determinant())

    def get_minor(self, row: int, column: int) -> int:
        values = [
            [
                self.rows[other_row][other_column]
                for other_column in range(self.num_columns)
                if other_column != column
            ]
            for other_row in range(self.num_rows)
            if other_row != row
        ]
        return Matrix(values).determinant()

    def get_cofactor(self, row: int, column: int) -> int:
        if (row + column) % 2 == 0:
            return self.get_minor(row, column)
        return -1 * self.get_minor(row, column)

    def minors(self) -> Matrix:
        return Matrix(
            [
                [self.get_minor(row, column) for column in range(self.num_columns)]
                for row in range(self.num_rows)
            ]
        )

    def cofactors(self) -> Matrix:
        return Matrix(
            [
                [
                    self.minors().rows[row][column]
                    if (row + column) % 2 == 0
                    else self.minors().rows[row][column] * -1
                    for column in range(self.minors().num_columns)
                ]
                for row in range(self.minors().num_rows)
            ]
        )

    def adjugate(self) -> Matrix:
        values = [
            [self.cofactors().rows[column][row] for column in range(self.num_columns)]
            for row in range(self.num_rows)
        ]
        return Matrix(values)

    def inverse(self) -> Matrix:
        determinant = self.determinant()
        if not determinant:
            raise TypeError("Only matrices with a non-zero determinant have an inverse")
        return self.adjugate() * (1 / determinant)

    def __repr__(self) -> str:
        return str(self.rows)

    def __str__(self) -> str:
        if self.num_rows == 0:
            return "[]"
        if self.num_rows == 1:
            return "[[" + ". ".join(str(self.rows[0])) + "]]"
        return (
            "["
            + "\n ".join(
                [
                    "[" + ". ".join([str(value) for value in row]) + ".]"
                    for row in self.rows
                ]
            )
            + "]"
        )

    def add_row(self, row: list[int], position: int | None = None) -> None:
        type_error = TypeError("Row must be a list containing all ints and/or floats")
        if not isinstance(row, list):
            raise type_error
        for value in row:
            if not isinstance(value, (int, float)):
                raise type_error
        if len(row) != self.num_columns:
            raise ValueError(
                "Row must be equal in length to the other rows in the matrix"
            )
        if position is None:
            self.rows.append(row)
        else:
            self.rows = [*self.rows[0:position], row, *self.rows[position:]]

    def add_column(self, column: list[int], position: int | None = None) -> None:
        type_error = TypeError(
            "Column must be a list containing all ints and/or floats"
        )
        if not isinstance(column, list):
            raise type_error
        for value in column:
            if not isinstance(value, (int, float)):
                raise type_error
        if len(column) != self.num_rows:
            raise ValueError(
                "Column must be equal in length to the other columns in the matrix"
            )
        if position is None:
            self.rows = [self.rows[i] + [column[i]] for i in range(self.num_rows)]
        else:
            self.rows = [
                [*self.rows[i][0:position], column[i], *self.rows[i][position:]]
                for i in range(self.num_rows)
            ]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self.rows == other.rows

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __neg__(self) -> Matrix:
        return self * -1

    def __add__(self, other: Matrix) -> Matrix:
        if self.order != other.order:
            raise ValueError("Addition requires matrices of the same order")
        return Matrix(
            [
                [self.rows[i][j] + other.rows[i][j] for j in range(self.num_columns)]
                for i in range(self.num_rows)
            ]
        )

    def __sub__(self, other: Matrix) -> Matrix:
        if self.order != other.order:
            raise ValueError("Subtraction requires matrices of the same order")
        return Matrix(
            [
                [self.rows[i][j] - other.rows[i][j] for j in range(self.num_columns)]
                for i in range(self.num_rows)
            ]
        )

    def __mul__(self, other: Matrix | float) -> Matrix:
        if isinstance(other, (int, float)):
            return Matrix(
                [[int(element * other) for element in row] for row in self.rows]
            )
        elif isinstance(other, Matrix):
            if self.num_columns != other.num_rows:
                raise ValueError(
                    "The number of columns in the first matrix must "
                    "be equal to the number of rows in the second"
                )
            return Matrix(
                [
                    [Matrix.dot_product(row, column) for column in other.columns()]
                    for row in self.rows
                ]
            )
        else:
            raise TypeError(
                "A Matrix can only be multiplied by an int, float, or another matrix"
            )

    def __pow__(self, other: int) -> Matrix:
        if not isinstance(other, int):
            raise TypeError("A Matrix can only be raised to the power of an int")
        if not self.is_square:
            raise ValueError("Only square matrices can be raised to a power")
        if other == 0:
            return self.identity()
        if other < 0:
            if self.is_invertable():
                return self.inverse() ** (-other)
            raise ValueError(
                "Only invertable matrices can be raised to a negative power"
            )
        result = self
        for _ in range(other - 1):
            result *= self
        return result

    @classmethod
    def dot_product(cls, row: list[int], column: list[int]) -> int:
        return sum(row[i] * column[i] for i in range(len(row)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
