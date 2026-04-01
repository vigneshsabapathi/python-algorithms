"""
Optimized binary insertion sort — three variants benchmarked.

Variants:
1. bisect_left + manual shift  — replaces the manual binary search loop with
   the C-level bisect.bisect_left, keeping the Python shift loop.
2. bisect.insort               — stdlib one-liner: finds insertion point AND
   shifts in a single C-level call.
3. sorted() / list.sort()      — Python's Timsort, included for context.

Interview takeaway:
- Binary insertion sort reduces *comparisons* from O(n) to O(log n) per step
  but shifting is still O(n) → overall O(n²).  Use it when comparisons are
  expensive (e.g. custom __lt__ with DB calls) and n is small-to-medium.
- bisect.insort is the Pythonic production answer.
- For general sorting, sorted() / list.sort() (Timsort O(n log n)) wins.
"""

from __future__ import annotations

import bisect


def binary_insertion_sort_bisect(collection: list) -> list:
    """
    Uses bisect.bisect_left for O(log n) position finding;
    keeps a Python-level shift loop.

    >>> binary_insertion_sort_bisect([0, 4, 1234, 4, 1])
    [0, 1, 4, 4, 1234]
    >>> binary_insertion_sort_bisect([]) == []
    True
    >>> binary_insertion_sort_bisect([-1, -2, -3])
    [-3, -2, -1]
    >>> binary_insertion_sort_bisect(['d', 'a', 'b', 'e', 'c'])
    ['a', 'b', 'c', 'd', 'e']
    """
    for i in range(1, len(collection)):
        value = collection[i]
        pos = bisect.bisect_left(collection, value, 0, i)
        collection[pos + 1 : i + 1] = collection[pos:i]   # slice shift (C-level)
        collection[pos] = value
    return collection


def binary_insertion_sort_insort(collection: list) -> list:
    """
    Uses bisect.insort: finds insertion point AND inserts in one C-level call.
    Most concise; avoids all Python-level looping for the inner step.

    >>> binary_insertion_sort_insort([0, 4, 1234, 4, 1])
    [0, 1, 4, 4, 1234]
    >>> binary_insertion_sort_insort([]) == []
    True
    >>> binary_insertion_sort_insort([-1, -2, -3])
    [-3, -2, -1]
    >>> binary_insertion_sort_insort(['d', 'a', 'b', 'e', 'c'])
    ['a', 'b', 'c', 'd', 'e']
    """
    result: list = []
    for item in collection:
        bisect.insort(result, item)
    return result


def benchmark() -> None:
    import random
    import timeit

    from sorts.binary_insertion_sort import binary_insertion_sort as orig

    random.seed(42)
    small = random.sample(range(1000), 50)
    medium = random.sample(range(10_000), 500)
    nearly = list(range(200)) + [198, 5, 201]   # nearly sorted

    n = 2_000

    datasets = [
        ("small  (n=50,  random)", small),
        ("medium (n=500, random)", medium),
        ("nearly sorted (n=203)", nearly),
    ]

    header = f"{'Dataset':<30} {'Original':>10} {'bisect_left':>12} {'insort':>10} {'sorted()':>10}"
    print(header)
    print("-" * len(header))

    for label, data in datasets:
        t_orig = timeit.timeit(lambda d=data: orig(list(d)), number=n)
        t_bl   = timeit.timeit(lambda d=data: binary_insertion_sort_bisect(list(d)), number=n)
        t_ins  = timeit.timeit(lambda d=data: binary_insertion_sort_insort(list(d)), number=n)
        t_sort = timeit.timeit(lambda d=data: sorted(d), number=n)
        print(f"{label:<30} {t_orig:>10.3f} {t_bl:>12.3f} {t_ins:>10.3f} {t_sort:>10.3f}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
