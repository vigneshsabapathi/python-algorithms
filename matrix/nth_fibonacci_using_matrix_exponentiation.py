"""

Task:
Find the nth Fibonacci number using matrix exponentiation.
Time: O(log n * 8) where 8 is the cost of 2x2 matrix multiplication.

Implementation notes: Uses the identity:
  [F(n), F(n-1)] = [[1,1],[1,0]]^(n-1) * [F(1), F(0)]
Matrix exponentiation via repeated squaring gives O(log n) performance,
compared to O(n) for the brute force iterative approach.

Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/nth_fibonacci_using_matrix_exponentiation.py
"""


def multiply(matrix_a: list[list[int]], matrix_b: list[list[int]]) -> list[list[int]]:
    """
    Multiply two square matrices.

    >>> multiply([[1, 1], [1, 0]], [[1, 1], [1, 0]])
    [[2, 1], [1, 1]]
    """
    matrix_c = []
    n = len(matrix_a)
    for i in range(n):
        row = []
        for j in range(n):
            val = 0
            for k in range(n):
                val += matrix_a[i][k] * matrix_b[k][j]
            row.append(val)
        matrix_c.append(row)
    return matrix_c


def identity(n: int) -> list[list[int]]:
    """
    >>> identity(2)
    [[1, 0], [0, 1]]
    """
    return [[int(row == column) for column in range(n)] for row in range(n)]


def nth_fibonacci_matrix(n: int) -> int:
    """
    Find nth Fibonacci number using matrix exponentiation.

    >>> nth_fibonacci_matrix(0)
    0
    >>> nth_fibonacci_matrix(1)
    1
    >>> nth_fibonacci_matrix(10)
    55
    >>> nth_fibonacci_matrix(100)
    354224848179261915075
    >>> nth_fibonacci_matrix(-100)
    -100
    """
    if n <= 1:
        return n
    res_matrix = identity(2)
    fibonacci_matrix = [[1, 1], [1, 0]]
    n = n - 1
    while n > 0:
        if n % 2 == 1:
            res_matrix = multiply(res_matrix, fibonacci_matrix)
        fibonacci_matrix = multiply(fibonacci_matrix, fibonacci_matrix)
        n = int(n / 2)
    return res_matrix[0][0]


def nth_fibonacci_bruteforce(n: int) -> int:
    """
    Find nth Fibonacci number using iterative approach.

    >>> nth_fibonacci_bruteforce(0)
    0
    >>> nth_fibonacci_bruteforce(1)
    1
    >>> nth_fibonacci_bruteforce(10)
    55
    >>> nth_fibonacci_bruteforce(100)
    354224848179261915075
    >>> nth_fibonacci_bruteforce(-100)
    -100
    """
    if n <= 1:
        return n
    fib0, fib1 = 0, 1
    for _ in range(2, n + 1):
        fib0, fib1 = fib1, fib0 + fib1
    return fib1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
