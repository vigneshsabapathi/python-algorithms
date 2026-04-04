"""
Double Linear Search.

Searches a list from both ends simultaneously.  Two pointers advance inward
from opposite ends; the search stops as soon as either pointer finds the item
or the pointers cross (item not present).

Advantage over a single-direction linear search:
  - Items near the END are found in O(k) steps where k is their distance
    from the nearest end, rather than O(n - k) steps from the left end alone.
  - On average, items are found twice as fast as a purely left-to-right scan.

Complexity:
  Time  : O(n) worst case (item in the exact middle, or not present).
          At most n//2 iterations, but each does 2 comparisons → n total.
  Space : O(1)

Note: works on any unsorted list.  For sorted lists, prefer binary search.
"""

from __future__ import annotations


def double_linear_search(array: list[int], search_item: int) -> int:
    """
    Search array from both ends simultaneously; return first matching index.

    When the item appears at both ends, the left (start_ind) result is returned
    because it is checked first in the loop body.

    :param array: the list to search (need not be sorted)
    :param search_item: the value to find
    :return: index of search_item, or -1 if not found

    Examples:
    >>> double_linear_search([1, 5, 5, 10], 1)
    0
    >>> double_linear_search([1, 5, 5, 10], 5)
    1
    >>> double_linear_search([1, 5, 5, 10], 100)
    -1
    >>> double_linear_search([1, 5, 5, 10], 10)
    3
    >>> double_linear_search([], 1)
    -1
    >>> double_linear_search([7], 7)
    0
    >>> double_linear_search([7], 9)
    -1
    >>> double_linear_search([3, 3], 3)
    0
    """
    start_ind, end_ind = 0, len(array) - 1
    while start_ind <= end_ind:
        if array[start_ind] == search_item:
            return start_ind
        elif array[end_ind] == search_item:
            return end_ind
        else:
            start_ind += 1
            end_ind -= 1
    return -1


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    examples = [
        (list(range(100)), 40),
        (list(range(100)), 99),   # near end: double search wins
        (list(range(100)), 0),    # at start: both find immediately
        ([1, 5, 5, 10], 5),
        ([], 1),
        ([42], 42),
    ]
    for arr, target in examples:
        result = double_linear_search(arr, target)
        print(f"double_linear_search(arr={arr[:5]}{'...' if len(arr)>5 else ''}, {target}) = {result}")
