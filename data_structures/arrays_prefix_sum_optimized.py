"""
Optimized variants of Prefix Sum.

Benchmarks three approaches: class-based, function-based, and itertools.accumulate.
"""

import itertools
import timeit


# Variant 1: Class-based (original)
class PrefixSumClass:
    """
    Class-based prefix sum with get_sum and contains_sum.
    Time: O(n) build, O(1) query, Space: O(n)

    >>> ps = PrefixSumClass([1, 2, 3, 4, 5])
    >>> ps.get_sum(1, 3)
    9
    >>> ps.contains_sum(6)
    True
    >>> ps.contains_sum(7)
    False
    """

    def __init__(self, array: list[int]) -> None:
        n = len(array)
        self.prefix_sum = [0] * n
        if n > 0:
            self.prefix_sum[0] = array[0]
        for i in range(1, n):
            self.prefix_sum[i] = self.prefix_sum[i - 1] + array[i]

    def get_sum(self, start: int, end: int) -> int:
        if not self.prefix_sum:
            raise ValueError("The array is empty.")
        if start < 0 or end >= len(self.prefix_sum) or start > end:
            raise ValueError("Invalid range specified.")
        if start == 0:
            return self.prefix_sum[end]
        return self.prefix_sum[end] - self.prefix_sum[start - 1]

    def contains_sum(self, target_sum: int) -> bool:
        sums = {0}
        for sum_item in self.prefix_sum:
            if sum_item - target_sum in sums:
                return True
            sums.add(sum_item)
        return False


# Variant 2: Function-based using itertools.accumulate
def build_prefix_accumulate(array: list[int]) -> list[int]:
    """
    Build prefix sum using itertools.accumulate.
    Time: O(n), Space: O(n)

    >>> build_prefix_accumulate([1, 2, 3, 4, 5])
    [1, 3, 6, 10, 15]
    >>> build_prefix_accumulate([])
    []
    """
    return list(itertools.accumulate(array))


def range_sum_accumulate(prefix: list[int], start: int, end: int) -> int:
    """
    Query sum in [start, end] from a prefix sum list.

    >>> p = build_prefix_accumulate([1, 2, 3, 4, 5])
    >>> range_sum_accumulate(p, 1, 3)
    9
    >>> range_sum_accumulate(p, 0, 4)
    15
    """
    if start == 0:
        return prefix[end]
    return prefix[end] - prefix[start - 1]


# Variant 3: Numpy-based (optional, with fallback)
def build_prefix_numpy(array: list[int]) -> list[int]:
    """
    Build prefix sum using numpy cumsum (if available), else fallback.
    Time: O(n), Space: O(n)

    >>> build_prefix_numpy([1, 2, 3, 4, 5])
    [1, 3, 6, 10, 15]
    """
    try:
        import numpy as np
        return np.cumsum(array).tolist()
    except ImportError:
        return list(itertools.accumulate(array))


def benchmark():
    data = list(range(1, 1001))  # [1..1000]
    n = 5000

    t1 = timeit.timeit(lambda: PrefixSumClass(data), number=n)
    t2 = timeit.timeit(lambda: build_prefix_accumulate(data), number=n)
    t3 = timeit.timeit(lambda: build_prefix_numpy(data), number=n)

    print(f"class-based:   {t1:.4f}s for {n} builds")
    print(f"accumulate:    {t2:.4f}s for {n} builds")
    print(f"numpy_cumsum:  {t3:.4f}s for {n} builds")


if __name__ == "__main__":
    benchmark()
