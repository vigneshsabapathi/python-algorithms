"""
Smallest Range Covering Elements from K Lists

Given k sorted lists, find the smallest range [a, b] that includes
at least one number from each of the k lists.

Greedy with min-heap: maintain one pointer per list, always advance
the minimum element, tracking the current range.

Reference: https://github.com/TheAlgorithms/Python/blob/master/greedy_methods/smallest_range.py

>>> smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]])
[20, 24]
>>> smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
[1, 1]
"""

import heapq


def smallest_range(nums: list[list[int]]) -> list[int]:
    """
    Find the smallest range that includes at least one number from each list.

    >>> smallest_range([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]])
    [20, 24]
    >>> smallest_range([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    [1, 1]
    >>> smallest_range([[1]])
    [1, 1]
    >>> smallest_range([[1, 5, 8], [4, 12], [7, 8, 10]])
    [4, 7]
    """
    # Min-heap: (value, list_index, element_index)
    heap: list[tuple[int, int, int]] = []
    current_max = float("-inf")

    # Initialize with first element from each list
    for i, lst in enumerate(nums):
        heapq.heappush(heap, (lst[0], i, 0))
        current_max = max(current_max, lst[0])

    best_range = [heap[0][0], current_max]

    while True:
        min_val, list_idx, elem_idx = heapq.heappop(heap)

        # If this list is exhausted, we're done
        if elem_idx + 1 >= len(nums[list_idx]):
            break

        # Advance pointer in the list that had the minimum
        next_val = nums[list_idx][elem_idx + 1]
        heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
        current_max = max(current_max, next_val)

        # Check if new range is smaller
        new_min = heap[0][0]
        if current_max - new_min < best_range[1] - best_range[0]:
            best_range = [new_min, current_max]

    return best_range


if __name__ == "__main__":
    import doctest

    doctest.testmod()
