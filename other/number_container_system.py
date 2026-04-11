"""
Number Container System — Data structure for index-to-number mapping with find-smallest.

Supports inserting/replacing numbers at indices and finding the smallest index
containing a given number.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/number_container_system.py
"""

from __future__ import annotations

import heapq
from collections import defaultdict


class NumberContainerSystem:
    """
    Number container supporting change and find operations.

    >>> nc = NumberContainerSystem()
    >>> nc.find(10)
    -1
    >>> nc.change(2, 10)
    >>> nc.change(1, 10)
    >>> nc.change(3, 10)
    >>> nc.change(5, 10)
    >>> nc.find(10)
    1
    >>> nc.change(1, 20)
    >>> nc.find(10)
    2
    """

    def __init__(self) -> None:
        self.index_to_num: dict[int, int] = {}
        self.num_to_indices: dict[int, list[int]] = defaultdict(list)

    def change(self, index: int, number: int) -> None:
        """Insert or replace the number at index."""
        self.index_to_num[index] = number
        heapq.heappush(self.num_to_indices[number], index)

    def find(self, number: int) -> int:
        """Find the smallest index with the given number, or -1."""
        while self.num_to_indices[number]:
            idx = self.num_to_indices[number][0]
            # Check if this index still holds the right number (lazy deletion)
            if self.index_to_num.get(idx) == number:
                return idx
            heapq.heappop(self.num_to_indices[number])
        return -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
