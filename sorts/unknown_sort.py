"""
Double-ended Selection Sort (file: unknown_sort.py).

Each iteration simultaneously extracts the minimum and maximum from the
remaining collection, appending the min to the front accumulator and the
max to the back accumulator.  After n//2 passes only 0 or 1 element is left;
that middle element (if any) is sandwiched between the two accumulators.

Despite being named merge_sort in some versions of this file, this is
NOT merge sort — it is a double-ended (bidirectional) selection sort.

Complexity (all cases):
    Time  : O(n^2) — min(), max(), and list.remove() are each O(n); the
            loop runs n//2 times.  The "best case O(n)" claim in older
            versions of this file is incorrect.
    Space : O(n)   — start and end lists together hold all n elements.
"""


def unknown_sort(collection: list) -> list:
    """Sort a list by repeatedly pulling the min and max from each end.

    Note: preserves duplicates correctly (remove() removes only the first
    occurrence, which matches the element chosen by min/max).

    >>> unknown_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> unknown_sort([])
    []

    >>> unknown_sort([-2, -5, -45])
    [-45, -5, -2]

    >>> unknown_sort([1])
    [1]

    >>> unknown_sort([3, 3, 3])
    [3, 3, 3]

    >>> unknown_sort([5, 3, 8, 1, 4])
    [1, 3, 4, 5, 8]

    >>> unknown_sort([10, -1, 0])
    [-1, 0, 10]
    """
    start: list = []
    end: list = []
    while len(collection) > 1:
        min_one, max_one = min(collection), max(collection)
        start.append(min_one)
        end.append(max_one)
        collection.remove(min_one)
        collection.remove(max_one)
    end.reverse()
    return start + collection + end


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    examples = [
        [5, 6, 1, -1, 4, 37, -3, 7],
        [0, 5, 3, 2, 2],
        [],
        [42],
        [3, 3, 3, 1, 2],
    ]
    for ex in examples:
        print(f"unknown_sort({ex}) = {unknown_sort(list(ex))}")
