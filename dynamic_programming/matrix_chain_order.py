"""
Matrix Chain Order — Returns both the cost matrix and the split matrix.

Unlike matrix_chain_multiplication.py which returns just the minimum cost,
this version returns the full DP tables, allowing reconstruction of the
optimal parenthesization.

Time Complexity: O(n^3)
Space Complexity: O(n^2)

>>> matrix_chain_order([10, 30, 5])
([[0, 0, 0], [0, 0, 1500], [0, 0, 0]], [[0, 0, 0], [0, 0, 1], [0, 0, 0]])
"""

from __future__ import annotations

import sys


def matrix_chain_order(
    array: list[int],
) -> tuple[list[list[int]], list[list[int]]]:
    """
    Return (cost_matrix, split_matrix) for matrix chain multiplication.

    >>> matrix_chain_order([10, 30, 5])
    ([[0, 0, 0], [0, 0, 1500], [0, 0, 0]], [[0, 0, 0], [0, 0, 1], [0, 0, 0]])
    """
    n = len(array)
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    sol = [[0 for _ in range(n)] for _ in range(n)]

    for chain_length in range(2, n):
        for a in range(1, n - chain_length + 1):
            b = a + chain_length - 1
            matrix[a][b] = sys.maxsize
            for c in range(a, b):
                cost = (
                    matrix[a][c]
                    + matrix[c + 1][b]
                    + array[a - 1] * array[c] * array[b]
                )
                if cost < matrix[a][b]:
                    matrix[a][b] = cost
                    sol[a][b] = c
    return matrix, sol


def print_optimal_solution(optimal_solution: list[list[int]], i: int, j: int) -> str:
    """
    Return a string showing the optimal parenthesization.

    >>> m, s = matrix_chain_order([30, 35, 15, 5, 10, 20, 25])
    >>> print_optimal_solution(s, 1, 6)
    '( ( A1 ( A2 A3 ) ) ( ( A4 A5 ) A6 ) )'
    """
    if i == j:
        return f"A{i}"
    else:
        left = print_optimal_solution(optimal_solution, i, optimal_solution[i][j])
        right = print_optimal_solution(
            optimal_solution, optimal_solution[i][j] + 1, j
        )
        return f"( {left} {right} )"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    array = [30, 35, 15, 5, 10, 20, 25]
    n = len(array)
    matrix, optimal_solution = matrix_chain_order(array)
    print(f"  No. of operations required: {matrix[1][n - 1]}")
    print(f"  Optimal parenthesization: {print_optimal_solution(optimal_solution, 1, n - 1)}")
