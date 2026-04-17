"""
Optimized variants of Kth Largest Element.

Find the kth largest element in an unsorted array.

Benchmarks three approaches using timeit.
"""

import heapq
import timeit


# Variant 1: QuickSelect — original O(n) average approach
def kth_largest_quickselect(arr: list[int], k: int) -> int:
    """
    QuickSelect partition-based approach.
    Time: O(n) average, O(n^2) worst, Space: O(1)

    >>> kth_largest_quickselect([3,1,4,1,5,9,2,6,5,3,5], 3)
    5
    >>> kth_largest_quickselect([2,1], 1)
    2
    """
    if not arr or not 1 <= k <= len(arr):
        return -1

    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] >= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    arr = list(arr)  # don't mutate original
    low, high = 0, len(arr) - 1
    while low <= high:
        pivot_idx = partition(low, high)
        if pivot_idx == k - 1:
            return arr[pivot_idx]
        elif pivot_idx > k - 1:
            high = pivot_idx - 1
        else:
            low = pivot_idx + 1
    return -1


# Variant 2: Sort and index — simple O(n log n)
def kth_largest_sort(arr: list[int], k: int) -> int:
    """
    Sort the array and return kth largest.
    Time: O(n log n), Space: O(n)

    >>> kth_largest_sort([3,1,4,1,5,9,2,6,5,3,5], 3)
    5
    >>> kth_largest_sort([2,1], 1)
    2
    """
    if not arr or not 1 <= k <= len(arr):
        return -1
    return sorted(arr, reverse=True)[k - 1]


# Variant 3: Min-heap of size k — O(n log k)
def kth_largest_heap(arr: list[int], k: int) -> int:
    """
    Use a min-heap of size k.
    Time: O(n log k), Space: O(k)

    >>> kth_largest_heap([3,1,4,1,5,9,2,6,5,3,5], 3)
    5
    >>> kth_largest_heap([2,1], 1)
    2
    """
    if not arr or not 1 <= k <= len(arr):
        return -1
    return heapq.nlargest(k, arr)[-1]


def benchmark():
    import random

    data = random.sample(range(10000), 1000)
    k = 10
    n = 500

    t1 = timeit.timeit(lambda: kth_largest_quickselect(data, k), number=n)
    t2 = timeit.timeit(lambda: kth_largest_sort(data, k), number=n)
    t3 = timeit.timeit(lambda: kth_largest_heap(data, k), number=n)

    print(f"quickselect: {t1:.4f}s for {n} runs")
    print(f"sort:        {t2:.4f}s for {n} runs")
    print(f"heap:        {t3:.4f}s for {n} runs")


if __name__ == "__main__":
    benchmark()
