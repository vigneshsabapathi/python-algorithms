# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/minimum_coin_change.py


def minimum_coin_change(coins: list[int], amount: int) -> int:
    """
    Find the minimum number of coins needed to make the given amount.
    Returns -1 if not possible.

    >>> minimum_coin_change([1, 5, 10, 25], 30)
    2
    >>> minimum_coin_change([1, 5, 10, 25], 11)
    2
    >>> minimum_coin_change([2], 3)
    -1
    >>> minimum_coin_change([1], 0)
    0
    >>> minimum_coin_change([1, 2, 5], 11)
    3
    >>> minimum_coin_change([186, 419, 83, 408], 6249)
    20
    """
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ([1, 5, 10, 25], 30, 2),
        ([1, 5, 10, 25], 11, 2),
        ([2], 3, -1),
        ([1], 0, 0),
        ([1, 2, 5], 11, 3),
        ([186, 419, 83, 408], 6249, 20),
    ]
    for coins, amount, expected in cases:
        result = minimum_coin_change(coins, amount)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] minimum_coin_change({coins}, {amount}) = {result}  (expected {expected})")
