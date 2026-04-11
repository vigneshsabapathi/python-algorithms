"""
Fractional Knapsack Problem

Given weights and values of n items, put them in a knapsack of capacity W.
Items can be broken into fractions — take as much of each item as you want.
Maximize total value.

Reference: https://github.com/TheAlgorithms/Python/blob/master/greedy_methods/fractional_knapsack.py

>>> fractional_knapsack([60, 100, 120], [10, 20, 30], 50)
240.0
>>> fractional_knapsack([500], [30], 10)
166.66666666666666
>>> fractional_knapsack([10, 20, 30], [5, 10, 15], 15)
30.0
"""


def fractional_knapsack(
    values: list[int],
    weights: list[int],
    capacity: int,
) -> float:
    """
    Greedy: sort items by value-to-weight ratio descending, take greedily.

    >>> fractional_knapsack([60, 100, 120], [10, 20, 30], 50)
    240.0
    >>> fractional_knapsack([500], [30], 10)
    166.66666666666666
    >>> fractional_knapsack([10, 20, 30], [5, 10, 15], 15)
    30.0
    >>> fractional_knapsack([], [], 50)
    0.0
    >>> fractional_knapsack([60, 100], [10, 20], 0)
    0.0
    >>> fractional_knapsack([60, 100, 120], [10, 20, 30], 60)
    280.0
    """
    # Create list of (value, weight) and sort by value/weight ratio desc
    items = sorted(
        zip(values, weights),
        key=lambda x: x[0] / x[1] if x[1] > 0 else float("inf"),
        reverse=True,
    )

    total_value = 0.0
    remaining = capacity

    for value, weight in items:
        if remaining <= 0:
            break
        if weight <= remaining:
            total_value += value
            remaining -= weight
        else:
            # Take fraction
            total_value += value * (remaining / weight)
            remaining = 0

    return total_value


if __name__ == "__main__":
    import doctest

    doctest.testmod()
