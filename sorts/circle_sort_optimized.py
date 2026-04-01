"""
Optimized circle sort variants for interview prep.

Circle sort compares elements at mirror positions (left/right) working
inward, recursively subdivides, and repeats until no swaps occur.
Complexity: O(n log n log n) average — worse than Timsort's O(n log n).

Improvements:
1. Iterative circle sort — replaces recursion with an explicit stack,
   eliminating Python function-call overhead per subdivision.
2. Comparison with sorted() to illustrate the practical gap.

Interview insight:
- Circle sort is a "sorting circle" variant of odd-even merge sort.
- Not used in production; shown here for algorithmic breadth.
- The key idea (compare opposite ends, recurse on halves) resembles
  bitonic sort but works on arbitrary-length arrays.
- Always prefer sorted() / list.sort() for production Python.
"""

from __future__ import annotations

from collections import deque


def circle_sort_iterative(collection: list) -> list:
    """
    Circle sort using an explicit stack instead of recursion.
    Avoids Python's per-call overhead for the inner subdivisions.

    >>> circle_sort_iterative([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> circle_sort_iterative([])
    []
    >>> circle_sort_iterative([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    >>> circle_sort_iterative([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> circle_sort_iterative([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> circle_sort_iterative([3, 3, 3])
    [3, 3, 3]
    """
    arr = list(collection)
    n = len(arr)
    if n < 2:
        return arr

    def _one_pass() -> bool:
        """Run one full circle-sort pass over arr; return True if any swap."""
        swapped = False
        stack: deque[tuple[int, int]] = deque([(0, n - 1)])

        while stack:
            low, high = stack.pop()
            if low >= high:
                continue

            left, right = low, high
            while left < right:
                if arr[left] > arr[right]:
                    arr[left], arr[right] = arr[right], arr[left]
                    swapped = True
                left += 1
                right -= 1

            # Odd-length segment: middle element vs its right neighbour
            if left == right and arr[left] > arr[right + 1]:
                arr[left], arr[right + 1] = arr[right + 1], arr[left]
                swapped = True

            mid = low + (high - low) // 2
            stack.append((low, mid))
            stack.append((mid + 1, high))

        return swapped

    while _one_pass():
        pass

    return arr


def benchmark() -> None:
    import random
    import timeit

    from sorts.circle_sort import circle_sort as orig

    random.seed(42)
    n_runs = 2_000

    datasets = {
        "random     n=100": random.sample(range(-500, 500), 100),
        "reversed   n=100": list(range(100, 0, -1)),
        "nearly srt n=100": list(range(98)) + [99, 98],
        "random     n=300": random.sample(range(-1500, 1500), 300),
    }

    hdr = f"{'Dataset':<22} {'recursive':>12} {'iterative':>12} {'sorted()':>10}"
    print(hdr)
    print("-" * len(hdr))
    for label, data in datasets.items():
        tr = timeit.timeit(lambda d=data: orig(list(d)), number=n_runs)
        ti = timeit.timeit(lambda d=data: circle_sort_iterative(list(d)), number=n_runs)
        ts = timeit.timeit(lambda d=data: sorted(d), number=n_runs)
        print(f"{label:<22} {tr:>12.3f} {ti:>12.3f} {ts:>10.3f}")

    print()
    print("Pass count comparison (random n=20):")
    sample = random.sample(range(100), 20)
    for label, fn in [("recursive", orig), ("iterative", circle_sort_iterative)]:
        arr = list(sample)
        result = fn(arr)
        print(f"  {label}: result correct = {result == sorted(sample)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
