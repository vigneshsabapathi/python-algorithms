"""
Integer Partition — Count partitions of a positive integer.

The number of partitions of n is the number of ways to write n as a sum
of positive integers (order does not matter).

Example: partition(5) = 7
  5, 4+1, 3+2, 3+1+1, 2+2+1, 2+1+1+1, 1+1+1+1+1

Uses the recurrence:
  The number of partitions of n into at least k parts equals the number
  of partitions into exactly k parts plus partitions into at least k-1 parts.

>>> partition(5)
7
>>> partition(7)
15
>>> partition(100)
190569292
>>> partition(1)
1
"""


def partition(m: int) -> int:
    """
    Return the number of partitions of integer m.

    >>> partition(5)
    7
    >>> partition(7)
    15
    >>> partition(100)
    190569292
    >>> partition(1)
    1
    """
    if m <= 0:
        raise ValueError("m must be a positive integer")

    memo: list[list[int]] = [[0 for _ in range(m)] for _ in range(m + 1)]
    for i in range(m + 1):
        memo[i][0] = 1

    for n in range(m + 1):
        for k in range(1, m):
            memo[n][k] += memo[n][k - 1]
            if n - k > 0:
                memo[n][k] += memo[n - k - 1][k]

    return memo[m][m - 1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    for n in [1, 5, 7, 10, 20, 50, 100]:
        print(f"  partition({n}) = {partition(n)}")
