"""
H-Index — Compute a researcher's h-index from citation counts.

A researcher has an h-index of h if h papers have at least h citations each,
and the remaining papers have no more than h citations each.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/h_index.py
"""

from __future__ import annotations


def h_index(citations: list[int]) -> int:
    """
    Compute h-index from a list of citation counts.

    >>> h_index([3, 0, 6, 1, 5])
    3
    >>> h_index([1, 3, 1])
    1
    >>> h_index([0, 0, 0])
    0
    >>> h_index([10, 8, 5, 4, 3])
    4
    >>> h_index([])
    0
    >>> h_index([100])
    1
    >>> h_index([0])
    0
    >>> h_index([1, 1, 1, 1, 1])
    1
    """
    if not citations:
        return 0

    sorted_citations = sorted(citations, reverse=True)
    h = 0
    for i, c in enumerate(sorted_citations):
        if c >= i + 1:
            h = i + 1
        else:
            break

    return h


def h_index_counting_sort(citations: list[int]) -> int:
    """
    Compute h-index in O(n) using counting sort approach.

    >>> h_index_counting_sort([3, 0, 6, 1, 5])
    3
    >>> h_index_counting_sort([1, 3, 1])
    1
    >>> h_index_counting_sort([0, 0, 0])
    0
    >>> h_index_counting_sort([10, 8, 5, 4, 3])
    4
    >>> h_index_counting_sort([])
    0
    """
    if not citations:
        return 0

    n = len(citations)
    # Bucket: papers[i] = number of papers with exactly i citations
    # papers[n] catches all papers with >= n citations
    papers = [0] * (n + 1)
    for c in citations:
        papers[min(c, n)] += 1

    # Walk from high to low, accumulating count
    total = 0
    for i in range(n, -1, -1):
        total += papers[i]
        if total >= i:
            return i

    return 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
