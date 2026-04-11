"""
Minimum Coin Change (Greedy approach)

Given coin denominations and a target amount, find the minimum number of coins
needed using a greedy strategy: always pick the largest denomination first.

Note: The greedy approach works optimally for canonical coin systems (e.g., US coins).
For arbitrary denominations, dynamic programming is needed for optimal results.

Reference: https://github.com/TheAlgorithms/Python/blob/master/greedy_methods/minimum_coin_change.py

>>> minimum_coin_change([1, 5, 10, 25], 36)
[25, 10, 1]
>>> minimum_coin_change([1, 5, 10, 25], 0)
[]
>>> minimum_coin_change([1, 5, 10, 25], 5)
[5]
"""


def minimum_coin_change(denominations: list[int], amount: int) -> list[int]:
    """
    Greedy coin change: sort denominations descending, greedily pick largest.

    Returns a list of coins used (largest first).

    >>> minimum_coin_change([1, 5, 10, 25], 36)
    [25, 10, 1]
    >>> minimum_coin_change([1, 5, 10, 25], 0)
    []
    >>> minimum_coin_change([1, 5, 10, 25], 5)
    [5]
    >>> minimum_coin_change([1, 5, 10, 25], 30)
    [25, 5]
    >>> minimum_coin_change([1, 5, 10, 25], 99)
    [25, 25, 25, 10, 10, 1, 1, 1, 1]
    >>> minimum_coin_change([1, 3, 4], 6)
    [4, 1, 1]
    >>> minimum_coin_change([1], 7)
    [1, 1, 1, 1, 1, 1, 1]
    """
    coins_used: list[int] = []
    sorted_denominations = sorted(denominations, reverse=True)

    remaining = amount
    for coin in sorted_denominations:
        while remaining >= coin:
            remaining -= coin
            coins_used.append(coin)

    return coins_used


if __name__ == "__main__":
    import doctest

    doctest.testmod()
