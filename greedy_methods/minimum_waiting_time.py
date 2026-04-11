"""
Minimum Waiting Time

Given a list of query durations, find the order that minimizes
the total waiting time. Each query must wait for all preceding
queries to complete.

Greedy insight: sort queries in ascending order — shortest first.

Reference: https://github.com/TheAlgorithms/Python/blob/master/greedy_methods/minimum_waiting_time.py

>>> minimum_waiting_time([3, 2, 1, 2, 6])
17
>>> minimum_waiting_time([1, 2, 3])
4
>>> minimum_waiting_time([5])
0
"""


def minimum_waiting_time(queries: list[int]) -> int:
    """
    Sort ascending, then each query at index i contributes its duration
    to all (n - 1 - i) subsequent queries.

    Total wait = sum(duration * (n - 1 - i) for i, duration in sorted queries)

    >>> minimum_waiting_time([3, 2, 1, 2, 6])
    17
    >>> minimum_waiting_time([1, 2, 3])
    4
    >>> minimum_waiting_time([5])
    0
    >>> minimum_waiting_time([])
    0
    >>> minimum_waiting_time([1, 1, 1, 1])
    6
    >>> minimum_waiting_time([5, 1])
    1
    """
    sorted_queries = sorted(queries)
    n = len(sorted_queries)
    total_wait = 0

    for i, duration in enumerate(sorted_queries):
        queries_left = n - 1 - i
        total_wait += duration * queries_left

    return total_wait


if __name__ == "__main__":
    import doctest

    doctest.testmod()
