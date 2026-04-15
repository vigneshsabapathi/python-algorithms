# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/minimum_tickets_cost.py


def minimum_tickets_cost(days: list[int], costs: list[int]) -> int:
    """
    Find the minimum cost to travel on all given days.

    costs[0] = 1-day pass, costs[1] = 7-day pass, costs[2] = 30-day pass

    >>> minimum_tickets_cost([1, 4, 6, 7, 8, 20], [2, 7, 15])
    11
    >>> minimum_tickets_cost([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15])
    17
    >>> minimum_tickets_cost([1], [2, 7, 15])
    2
    >>> minimum_tickets_cost([], [2, 7, 15])
    0
    """
    if not days:
        return 0

    last_day = days[-1]
    travel_days = set(days)
    dp = [0] * (last_day + 1)

    for i in range(1, last_day + 1):
        if i not in travel_days:
            dp[i] = dp[i - 1]
        else:
            dp[i] = min(
                dp[i - 1] + costs[0],
                dp[max(0, i - 7)] + costs[1],
                dp[max(0, i - 30)] + costs[2],
            )

    return dp[last_day]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ([1, 4, 6, 7, 8, 20], [2, 7, 15], 11),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15], 17),
        ([1], [2, 7, 15], 2),
        ([], [2, 7, 15], 0),
    ]
    for days, costs, expected in cases:
        result = minimum_tickets_cost(days, costs)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] days={days}, costs={costs} = {result}  (expected {expected})")
