"""
Double Linear Search — Recursive implementation.

Searches from both ends simultaneously using recursion.  Each call advances
the left pointer forward and the right pointer backward until either end finds
the key or the pointers cross.

Known bugs:
  1. Sentinel collision: `right = right or len(list_data) - 1` uses 0 as the
     "uninitialized" sentinel.  Passing an explicit right=0 (e.g. to search
     only the first element) resets right to len-1.  Fix: use right=-1 and
     check `if right < 0`.
  2. RecursionError for n > ~2000: recursion depth is n//2, which exceeds
     Python's default limit of 1000 for arrays longer than ~2000 elements.
  3. Does NOT guarantee leftmost index when duplicates exist.
"""
from __future__ import annotations


def search(list_data: list, key: int, left: int = 0, right: int = 0) -> int:
    """
    Recursive double linear search: check both ends, recurse inward.

    :param list_data: the list to be searched
    :param key: the key to be searched
    :param left: the index of the left (start) pointer
    :param right: the index of the right (end) pointer (0 = auto-initialize)
    :return: index of key if found, else -1

    >>> search(list(range(0, 11)), 5)
    5
    >>> search([1, 2, 4, 5, 3], 4)
    2
    >>> search([1, 2, 4, 5, 3], 6)
    -1
    >>> search([5], 5)
    0
    >>> search([], 1)
    -1
    """
    right = right or len(list_data) - 1
    if left > right:
        return -1
    elif list_data[left] == key:
        return left
    elif list_data[right] == key:
        return right
    else:
        return search(list_data, key, left + 1, right - 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    examples = [
        (list(range(11)), 5),
        ([1, 2, 4, 5, 3], 4),
        ([1, 2, 4, 5, 3], 6),
        ([5], 5),
        ([], 1),
        ([1, 5, 5, 10], 10),   # near end — right pointer finds in 1 call
    ]
    for arr, key in examples:
        print(f"search({arr}, {key}) = {search(arr, key)}")
