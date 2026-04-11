"""

Task:
Find the inverse of a 2x2 or 3x3 matrix. A matrix multiplied with its
inverse gives the identity matrix. If the determinant is 0, no inverse exists.

Implementation notes: Uses Decimal for float precision. For 2x2, swaps and
negates elements. For 3x3, computes cofactor matrix, transposes (adjoint),
and divides by determinant.

Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/inverse_of_matrix.py
"""

from __future__ import annotations

from decimal import Decimal


def inverse_of_matrix(matrix: list[list[float]]) -> list[list[float]]:
    """
    Find the inverse of a 2x2 or 3x3 matrix.

    >>> inverse_of_matrix([[2, 5], [2, 0]])
    [[0.0, 0.5], [0.2, -0.2]]
    >>> inverse_of_matrix([[2.5, 5], [1, 2]])
    Traceback (most recent call last):
        ...
    ValueError: This matrix has no inverse.
    >>> inverse_of_matrix([[2, 5, 7], [2, 0, 1], [1, 2, 3]])
    [[2.0, 1.0, -5.0], [5.0, 1.0, -12.0], [-4.0, -1.0, 10.0]]
    >>> inverse_of_matrix([[1, 2, 2], [1, 2, 2], [3, 2, -1]])
    Traceback (most recent call last):
        ...
    ValueError: This matrix has no inverse.
    >>> inverse_of_matrix([[],[]])
    Traceback (most recent call last):
        ...
    ValueError: Please provide a matrix of size 2x2 or 3x3.
    >>> inverse_of_matrix([[1, 2], [3, 4], [5, 6]])
    Traceback (most recent call last):
        ...
    ValueError: Please provide a matrix of size 2x2 or 3x3.
    >>> inverse_of_matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    """
    d = Decimal

    if len(matrix) == 2 and len(matrix[0]) == 2 and len(matrix[1]) == 2:
        determinant = float(
            d(matrix[0][0]) * d(matrix[1][1]) - d(matrix[1][0]) * d(matrix[0][1])
        )
        if determinant == 0:
            raise ValueError("This matrix has no inverse.")

        swapped_matrix = [[0.0, 0.0], [0.0, 0.0]]
        swapped_matrix[0][0], swapped_matrix[1][1] = matrix[1][1], matrix[0][0]
        swapped_matrix[1][0], swapped_matrix[0][1] = -matrix[1][0], -matrix[0][1]

        return [
            [(float(d(n)) / determinant) or 0.0 for n in row] for row in swapped_matrix
        ]
    elif (
        len(matrix) == 3
        and len(matrix[0]) == 3
        and len(matrix[1]) == 3
        and len(matrix[2]) == 3
    ):
        determinant = float(
            (
                (d(matrix[0][0]) * d(matrix[1][1]) * d(matrix[2][2]))
                + (d(matrix[0][1]) * d(matrix[1][2]) * d(matrix[2][0]))
                + (d(matrix[0][2]) * d(matrix[1][0]) * d(matrix[2][1]))
            )
            - (
                (d(matrix[0][2]) * d(matrix[1][1]) * d(matrix[2][0]))
                + (d(matrix[0][1]) * d(matrix[1][0]) * d(matrix[2][2]))
                + (d(matrix[0][0]) * d(matrix[1][2]) * d(matrix[2][1]))
            )
        )
        if determinant == 0:
            raise ValueError("This matrix has no inverse.")

        cofactor_matrix = [[d(0.0)] * 3 for _ in range(3)]
        cofactor_matrix[0][0] = (d(matrix[1][1]) * d(matrix[2][2])) - (d(matrix[1][2]) * d(matrix[2][1]))
        cofactor_matrix[0][1] = -((d(matrix[1][0]) * d(matrix[2][2])) - (d(matrix[1][2]) * d(matrix[2][0])))
        cofactor_matrix[0][2] = (d(matrix[1][0]) * d(matrix[2][1])) - (d(matrix[1][1]) * d(matrix[2][0]))
        cofactor_matrix[1][0] = -((d(matrix[0][1]) * d(matrix[2][2])) - (d(matrix[0][2]) * d(matrix[2][1])))
        cofactor_matrix[1][1] = (d(matrix[0][0]) * d(matrix[2][2])) - (d(matrix[0][2]) * d(matrix[2][0]))
        cofactor_matrix[1][2] = -((d(matrix[0][0]) * d(matrix[2][1])) - (d(matrix[0][1]) * d(matrix[2][0])))
        cofactor_matrix[2][0] = (d(matrix[0][1]) * d(matrix[1][2])) - (d(matrix[0][2]) * d(matrix[1][1]))
        cofactor_matrix[2][1] = -((d(matrix[0][0]) * d(matrix[1][2])) - (d(matrix[0][2]) * d(matrix[1][0])))
        cofactor_matrix[2][2] = (d(matrix[0][0]) * d(matrix[1][1])) - (d(matrix[0][1]) * d(matrix[1][0]))

        # Transpose cofactor matrix to get adjoint, then divide by determinant
        inverse_matrix = [[d(0.0)] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                inverse_matrix[i][j] = cofactor_matrix[j][i] / d(determinant)

        return [[float(d(n)) or 0.0 for n in row] for row in inverse_matrix]
    raise ValueError("Please provide a matrix of size 2x2 or 3x3.")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
