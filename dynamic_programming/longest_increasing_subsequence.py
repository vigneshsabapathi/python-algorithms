"""
Longest Increasing Subsequence (LIS) — Recursive approach.

Given an array, find the longest strictly increasing subsequence.

Example: [10, 22, 9, 33, 21, 50, 41, 60, 80] -> [10, 22, 33, 41, 60, 80]

This uses a recursive divide-and-conquer approach.

>>> longest_subsequence([10, 22, 9, 33, 21, 50, 41, 60, 80])
[10, 22, 33, 41, 60, 80]
>>> longest_subsequence([4, 8, 7, 5, 1, 12, 2, 3, 9])
[1, 2, 3, 9]
>>> longest_subsequence([9, 8, 7, 6, 5, 7])
[5, 7]
>>> longest_subsequence([1, 1, 1])
[1, 1, 1]
>>> longest_subsequence([])
[]
"""

from __future__ import annotations


def longest_subsequence(array: list[int]) -> list[int]:
    """
    Find the longest increasing subsequence using recursion.

    >>> longest_subsequence([10, 22, 9, 33, 21, 50, 41, 60, 80])
    [10, 22, 33, 41, 60, 80]
    >>> longest_subsequence([4, 8, 7, 5, 1, 12, 2, 3, 9])
    [1, 2, 3, 9]
    >>> longest_subsequence([28, 26, 12, 23, 35, 39])
    [12, 23, 35, 39]
    >>> longest_subsequence([])
    []
    """
    array_length = len(array)
    if array_length <= 1:
        return array

    pivot = array[0]
    is_found = False
    i = 1
    longest_subseq: list[int] = []
    while not is_found and i < array_length:
        if array[i] < pivot:
            is_found = True
            temp_array = array[i:]
            temp_array = longest_subsequence(temp_array)
            if len(temp_array) > len(longest_subseq):
                longest_subseq = temp_array
        else:
            i += 1

    temp_array = [element for element in array[1:] if element >= pivot]
    temp_array = [pivot, *longest_subsequence(temp_array)]
    if len(temp_array) > len(longest_subseq):
        return temp_array
    else:
        return longest_subseq


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    tests = [
        [10, 22, 9, 33, 21, 50, 41, 60, 80],
        [4, 8, 7, 5, 1, 12, 2, 3, 9],
        [9, 8, 7, 6, 5, 7],
        [1, 2, 3, 4, 5],
    ]
    for arr in tests:
        print(f"  LIS({arr}) = {longest_subsequence(arr)}")
