"""
Optimized variants of Heap (Max Heap).

Three implementations:
1. Custom max heap (original)
2. Python heapq-based (negated for max)
3. Sorted list approach (baseline)

Benchmarks using timeit.
"""

import heapq
import timeit


# Variant 1: Custom max heap
class MaxHeap:
    """
    Custom max-heap implementation.
    Insert: O(log n), Extract-max: O(log n)

    >>> h = MaxHeap()
    >>> h.insert(5)
    >>> h.insert(3)
    >>> h.insert(8)
    >>> h.extract_max()
    8
    >>> h.extract_max()
    5
    """

    def __init__(self) -> None:
        self.heap: list[int] = []

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self.heap[i] > self.heap[parent]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i: int) -> None:
        n = len(self.heap)
        while True:
            largest = i
            left, right = 2 * i + 1, 2 * i + 2
            if left < n and self.heap[left] > self.heap[largest]:
                largest = left
            if right < n and self.heap[right] > self.heap[largest]:
                largest = right
            if largest == i:
                break
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            i = largest

    def insert(self, val: int) -> None:
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def extract_max(self) -> int:
        if not self.heap:
            raise IndexError("Heap is empty")
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        val = self.heap.pop()
        if self.heap:
            self._sift_down(0)
        return val

    def peek(self) -> int:
        return self.heap[0]


# Variant 2: heapq-based (negated for max-heap)
class HeapqMaxHeap:
    """
    Max-heap using Python's heapq (values negated).
    Insert: O(log n), Extract-max: O(log n)

    >>> h = HeapqMaxHeap()
    >>> h.insert(5)
    >>> h.insert(3)
    >>> h.insert(8)
    >>> h.extract_max()
    8
    >>> h.extract_max()
    5
    """

    def __init__(self) -> None:
        self._data: list[int] = []

    def insert(self, val: int) -> None:
        heapq.heappush(self._data, -val)

    def extract_max(self) -> int:
        if not self._data:
            raise IndexError("Heap is empty")
        return -heapq.heappop(self._data)

    def peek(self) -> int:
        return -self._data[0]


# Variant 3: Sorted list approach (baseline, for comparison)
class SortedListMaxHeap:
    """
    Max-heap using sorted list — simple but O(n) insert.
    Insert: O(n), Extract-max: O(1)

    >>> h = SortedListMaxHeap()
    >>> h.insert(5)
    >>> h.insert(3)
    >>> h.insert(8)
    >>> h.extract_max()
    8
    >>> h.extract_max()
    5
    """

    def __init__(self) -> None:
        self._data: list[int] = []

    def insert(self, val: int) -> None:
        import bisect
        bisect.insort(self._data, val)

    def extract_max(self) -> int:
        if not self._data:
            raise IndexError("Heap is empty")
        return self._data.pop()

    def peek(self) -> int:
        return self._data[-1]


def benchmark():
    import random
    data = random.sample(range(10000), 500)
    n = 1000

    def run_custom():
        h = MaxHeap()
        for v in data:
            h.insert(v)
        result = []
        while h.heap:
            result.append(h.extract_max())
        return result

    def run_heapq():
        h = HeapqMaxHeap()
        for v in data:
            h.insert(v)
        result = []
        while h._data:
            result.append(h.extract_max())
        return result

    def run_sorted():
        h = SortedListMaxHeap()
        for v in data:
            h.insert(v)
        result = []
        while h._data:
            result.append(h.extract_max())
        return result

    t1 = timeit.timeit(run_custom, number=n)
    t2 = timeit.timeit(run_heapq, number=n)
    t3 = timeit.timeit(run_sorted, number=n)

    print(f"custom_max_heap:  {t1:.4f}s for {n} runs")
    print(f"heapq_negated:    {t2:.4f}s for {n} runs")
    print(f"sorted_list:      {t3:.4f}s for {n} runs")


if __name__ == "__main__":
    benchmark()
