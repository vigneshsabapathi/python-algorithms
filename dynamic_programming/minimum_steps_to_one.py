# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/minimum_steps_to_one.py


def minimum_steps_to_one(n: int) -> int:
    """
    Find minimum steps to reduce n to 1 using these operations:
    1. Subtract 1
    2. Divide by 2 (if divisible)
    3. Divide by 3 (if divisible)

    >>> minimum_steps_to_one(1)
    0
    >>> minimum_steps_to_one(10)
    3
    >>> minimum_steps_to_one(15)
    4
    >>> minimum_steps_to_one(6)
    2
    >>> minimum_steps_to_one(2)
    1
    >>> minimum_steps_to_one(4)
    2
    """
    if n <= 1:
        return 0

    dp = [0] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + 1
        if i % 2 == 0:
            dp[i] = min(dp[i], dp[i // 2] + 1)
        if i % 3 == 0:
            dp[i] = min(dp[i], dp[i // 3] + 1)

    return dp[n]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        (1, 0), (10, 3), (15, 4), (6, 2), (2, 1), (4, 2),
    ]
    for n, expected in cases:
        result = minimum_steps_to_one(n)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] minimum_steps_to_one({n}) = {result}  (expected {expected})")
