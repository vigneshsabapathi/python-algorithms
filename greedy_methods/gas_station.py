"""
Gas Station (Circuit Tour) — LeetCode 134

There are n gas stations along a circular route. You start with an empty tank.
gas[i] = fuel at station i, cost[i] = fuel to travel from station i to i+1.
Return the starting station index if you can complete the circuit, else -1.

Reference: https://github.com/TheAlgorithms/Python/blob/master/greedy_methods/gas_station.py

>>> can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
3
>>> can_complete_circuit([2, 3, 4], [3, 4, 3])
-1
>>> can_complete_circuit([5, 1, 2, 3, 4], [4, 4, 1, 5, 1])
4
"""


def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    """
    Greedy single-pass: if total gas >= total cost, a solution exists.
    Track the current tank; if it goes negative, restart from the next station.

    >>> can_complete_circuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    3
    >>> can_complete_circuit([2, 3, 4], [3, 4, 3])
    -1
    >>> can_complete_circuit([5, 1, 2, 3, 4], [4, 4, 1, 5, 1])
    4
    >>> can_complete_circuit([5], [4])
    0
    >>> can_complete_circuit([1, 2], [2, 1])
    1
    >>> can_complete_circuit([], [])
    0
    """
    if not gas:
        return 0

    total_tank = 0
    current_tank = 0
    start = 0

    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total_tank += diff
        current_tank += diff

        if current_tank < 0:
            # Can't reach station i+1 from current start
            start = i + 1
            current_tank = 0

    return start if total_tank >= 0 else -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
