"""
Fractional Cover Problem (Set Cover variant with fractional selection)

Given a universe of elements and a collection of sets with associated costs,
find the minimum cost to cover all elements. Each set can be partially used
(fractional selection allowed).

The greedy approach: repeatedly pick the set with the best cost-effectiveness
(cost per uncovered element), covering as many remaining elements as possible.

Reference: https://github.com/TheAlgorithms/Python/blob/master/greedy_methods/fractional_cover_problem.py

>>> fractional_cover(
...     universe={1, 2, 3, 4, 5},
...     subsets=[{1, 2, 3}, {2, 4}, {3, 4, 5}],
...     costs=[5, 10, 3]
... )
8.0
"""


def fractional_cover(
    universe: set[int],
    subsets: list[set[int]],
    costs: list[float],
) -> float:
    """
    Greedy set cover: always pick the most cost-effective set for
    remaining uncovered elements.

    This implementation uses integer/full set selection (the standard
    greedy set cover), which gives a ln(n)-approximation.

    >>> fractional_cover({1, 2, 3, 4, 5}, [{1, 2, 3}, {2, 4}, {3, 4, 5}], [5, 10, 3])
    8.0
    >>> fractional_cover({1, 2, 3}, [{1, 2}, {2, 3}, {1, 3}], [1, 1, 1])
    2.0
    >>> fractional_cover({1}, [{1}], [7])
    7.0
    >>> fractional_cover(set(), [], [])
    0.0
    """
    uncovered = set(universe)
    total_cost = 0.0

    while uncovered:
        # Find the most cost-effective set
        best_idx = -1
        best_ratio = float("inf")

        for i, (subset, cost) in enumerate(zip(subsets, costs)):
            covered = subset & uncovered
            if covered:
                ratio = cost / len(covered)
                if ratio < best_ratio:
                    best_ratio = ratio
                    best_idx = i

        if best_idx == -1:
            break  # No set can cover remaining elements

        uncovered -= subsets[best_idx]
        total_cost += costs[best_idx]

    return total_cost


if __name__ == "__main__":
    import doctest

    doctest.testmod()
