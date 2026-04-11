"""
Best Time to Buy and Sell Stock

Given a list of stock prices where prices[i] is the price on day i,
find the maximum profit from a single buy-sell transaction.
You must buy before you sell.

Reference: https://github.com/TheAlgorithms/Python/blob/master/greedy_methods/best_time_to_buy_and_sell_stock.py

>>> max_profit([7, 1, 5, 3, 6, 4])
5
>>> max_profit([7, 6, 4, 3, 1])
0
>>> max_profit([2, 4, 1])
2
>>> max_profit([])
0
>>> max_profit([1])
0
>>> max_profit([1, 2])
1
"""


def max_profit(prices: list[int]) -> int:
    """
    Track the minimum price seen so far and the maximum profit achievable.
    Greedy: at each step, either update the minimum or check if selling
    at the current price yields a better profit.

    >>> max_profit([7, 1, 5, 3, 6, 4])
    5
    >>> max_profit([7, 6, 4, 3, 1])
    0
    >>> max_profit([2, 4, 1])
    2
    >>> max_profit([])
    0
    >>> max_profit([1])
    0
    >>> max_profit([1, 2])
    1
    >>> max_profit([3, 3, 3])
    0
    >>> max_profit([1, 2, 3, 4, 5])
    4
    """
    if len(prices) < 2:
        return 0

    min_price = prices[0]
    max_gain = 0

    for price in prices[1:]:
        max_gain = max(max_gain, price - min_price)
        min_price = min(min_price, price)

    return max_gain


if __name__ == "__main__":
    import doctest

    doctest.testmod()
