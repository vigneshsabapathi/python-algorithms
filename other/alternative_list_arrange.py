"""
Alternative List Arrange — Rearrange a list so that elements alternate
between the first half and the second half.

Given a list, rearrange it so the first element comes from the first half,
the second from the second half, and so on.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/alternative_list_arrange.py
"""

from __future__ import annotations


def alternative_list_arrange(lst: list) -> list:
    """
    Rearrange list by interleaving first half and second half.

    >>> alternative_list_arrange([1, 2, 3, 4, 5, 6])
    [1, 4, 2, 5, 3, 6]
    >>> alternative_list_arrange([1, 2, 3, 4, 5])
    [1, 4, 2, 5, 3]
    >>> alternative_list_arrange([])
    []
    >>> alternative_list_arrange([1])
    [1]
    >>> alternative_list_arrange([1, 2])
    [1, 2]
    >>> alternative_list_arrange([11, 22, 33, 44])
    [11, 33, 22, 44]
    """
    if len(lst) <= 1:
        return lst

    mid = (len(lst) + 1) // 2
    first_half = lst[:mid]
    second_half = lst[mid:]

    result = []
    for i in range(max(len(first_half), len(second_half))):
        if i < len(first_half):
            result.append(first_half[i])
        if i < len(second_half):
            result.append(second_half[i])

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
