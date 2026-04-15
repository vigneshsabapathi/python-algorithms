"""
Print Multiplication Table
==========================
"""
from typing import List


def multiplication_table(n: int, size: int = 10) -> List[str]:
    """
    Return rows of the multiplication table for ``n`` up to ``size``.

    >>> multiplication_table(3, 3)
    ['3 x 1 = 3', '3 x 2 = 6', '3 x 3 = 9']
    >>> multiplication_table(7, 1)
    ['7 x 1 = 7']
    """
    if size < 1:
        raise ValueError("size must be >= 1")
    return [f"{n} x {i} = {n * i}" for i in range(1, size + 1)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for line in multiplication_table(9, 10):
        print(line)
