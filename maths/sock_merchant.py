"""
Sock Merchant (HackerRank)
==========================
Given a list of sock colors, return the number of matched pairs.
"""
from collections import Counter
from typing import List


def sock_merchant(socks: List[int]) -> int:
    """
    >>> sock_merchant([10, 20, 20, 10, 10, 30, 50, 10, 20])
    3
    >>> sock_merchant([])
    0
    >>> sock_merchant([1, 1, 1, 1])
    2
    >>> sock_merchant([1, 2, 3])
    0
    """
    return sum(c // 2 for c in Counter(socks).values())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(sock_merchant([10, 20, 20, 10, 10, 30, 50, 10, 20]))
