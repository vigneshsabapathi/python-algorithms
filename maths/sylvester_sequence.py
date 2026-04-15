"""
Sylvester's Sequence
====================
a_1 = 2, a_{n+1} = a_n^2 - a_n + 1.

Yields 2, 3, 7, 43, 1807, 3263443, ...
"""
from typing import List


def sylvester(n: int) -> List[int]:
    """
    Return the first ``n`` terms of Sylvester's sequence.

    >>> sylvester(1)
    [2]
    >>> sylvester(5)
    [2, 3, 7, 43, 1807]
    >>> sylvester(0)
    []
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    out: List[int] = []
    cur = 2
    for _ in range(n):
        out.append(cur)
        cur = cur * cur - cur + 1
    return out


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for v in sylvester(7):
        print(v)
