"""
Optimal Merge Pattern (Minimum Cost to Merge Files)

Given n sorted files of different sizes, merge them into a single file
with minimum total merge cost. Each merge of two files of sizes m and n
costs m + n.

Greedy: always merge the two smallest files first (use a min-heap).
This is equivalent to building an optimal Huffman tree.

Reference: https://github.com/TheAlgorithms/Python/blob/master/greedy_methods/optimal_merge_pattern.py

>>> optimal_merge_cost([2, 3, 4, 5, 6, 7])
68
>>> optimal_merge_cost([5, 10, 20, 30, 30])
205
>>> optimal_merge_cost([10])
0
"""

import heapq


def optimal_merge_cost(files: list[int]) -> int:
    """
    Minimum cost to merge all files using a min-heap.

    >>> optimal_merge_cost([2, 3, 4, 5, 6, 7])
    68
    >>> optimal_merge_cost([5, 10, 20, 30, 30])
    205
    >>> optimal_merge_cost([10])
    0
    >>> optimal_merge_cost([])
    0
    >>> optimal_merge_cost([1, 1])
    2
    >>> optimal_merge_cost([1, 2, 3])
    9
    """
    if len(files) <= 1:
        return 0

    heap = list(files)
    heapq.heapify(heap)
    total_cost = 0

    while len(heap) > 1:
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)
        merge_cost = first + second
        total_cost += merge_cost
        heapq.heappush(heap, merge_cost)

    return total_cost


if __name__ == "__main__":
    import doctest

    doctest.testmod()
