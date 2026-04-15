# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/rod_cutting.py


def rod_cutting(prices: list[int], length: int) -> int:
    """
    Find the maximum revenue obtainable by cutting a rod and selling pieces.

    prices[i] = price of a rod of length i+1.

    >>> rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 8)
    22
    >>> rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 4)
    10
    >>> rod_cutting([3, 5, 8, 9, 10, 17, 17, 20], 1)
    3
    >>> rod_cutting([1], 1)
    1
    >>> rod_cutting([], 0)
    0
    """
    if length == 0:
        return 0

    dp = [0] * (length + 1)
    for i in range(1, length + 1):
        for j in range(i):
            if j < len(prices):
                dp[i] = max(dp[i], prices[j] + dp[i - j - 1])

    return dp[length]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    prices = [1, 5, 8, 9, 10, 17, 17, 20]
    cases = [
        (prices, 8, 22), (prices, 4, 10), ([3, 5, 8, 9, 10, 17, 17, 20], 1, 3),
        ([1], 1, 1), ([], 0, 0),
    ]
    for p, n, expected in cases:
        result = rod_cutting(p, n)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] rod_cutting(prices, {n}) = {result}  (expected {expected})")
