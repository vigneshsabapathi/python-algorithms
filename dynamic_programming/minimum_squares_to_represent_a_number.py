# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/minimum_squares_to_represent_a_number.py

import math


def minimum_squares(n: int) -> int:
    """
    Find the minimum number of perfect squares that sum to n.

    Lagrange's four-square theorem guarantees the answer is at most 4.

    >>> minimum_squares(12)
    3
    >>> minimum_squares(13)
    2
    >>> minimum_squares(1)
    1
    >>> minimum_squares(0)
    0
    >>> minimum_squares(7)
    4
    >>> minimum_squares(4)
    1
    >>> minimum_squares(100)
    1
    """
    if n <= 0:
        return 0

    dp = list(range(n + 1))  # worst case: all 1s

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return dp[n]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        (12, 3),
        (13, 2),
        (1, 1),
        (0, 0),
        (7, 4),
        (4, 1),
        (100, 1),
    ]
    for n, expected in cases:
        result = minimum_squares(n)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] minimum_squares({n}) = {result}  (expected {expected})")
