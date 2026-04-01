"""
Optimized bead sort using column-count reconstruction.

The original simulates n gravity passes (O(n²)). This version:
1. Counts beads per column in one forward pass: count[j] = # elements > j
2. Reconstructs each row from the bottom as the number of columns still
   carrying beads at that level.

Complexity: O(n × max_val) time, O(max_val) space.
Faster than O(n²) when max_val << n; slower when max_val >> n.

https://en.wikipedia.org/wiki/Bead_sort
"""


def bead_sort(sequence: list) -> list:
    """
    >>> bead_sort([6, 11, 12, 4, 1, 5])
    [1, 4, 5, 6, 11, 12]
    >>> bead_sort([9, 8, 7, 6, 5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> bead_sort([5, 0, 4, 3])
    [0, 3, 4, 5]
    >>> bead_sort([8, 2, 1])
    [1, 2, 8]
    >>> bead_sort([0, 0, 0])
    [0, 0, 0]
    >>> bead_sort([])
    []
    >>> bead_sort([1, .9, 0.0, 0, -1, -.9])
    Traceback (most recent call last):
        ...
    TypeError: Sequence must be list of non-negative integers
    """
    if any(not isinstance(x, int) or x < 0 for x in sequence):
        raise TypeError("Sequence must be list of non-negative integers")
    if not sequence:
        return sequence

    max_val = max(sequence)
    if max_val == 0:
        return list(sequence)

    n = len(sequence)

    # count[j] = number of elements with value > j
    # = number of beads in column j after gravity
    count = [0] * max_val
    for val in sequence:
        for j in range(val):
            count[j] += 1

    # Each row i (0 = bottom = smallest) holds beads from every column where
    # count[j] > i.  Row value = number of such columns.
    return [sum(1 for c in count if c > i) for i in range(n - 1, -1, -1)]


def benchmark() -> None:
    import timeit

    from sorts.bead_sort import bead_sort as orig

    # Dense: large n, small max_val  → optimized should win
    dense = list(range(200, 0, -1))          # 200 elements, max=200
    # Sparse: small n, large max_val → original should win
    sparse = [1000, 500, 750, 250, 900]      # 5 elements, max=1000
    n = 5_000

    print("Dense case (n=200, max_val=200):")
    t_orig = timeit.timeit(lambda: orig(list(dense)), number=n)
    t_opt = timeit.timeit(lambda: bead_sort(list(dense)), number=n)
    print(f"  original (n² passes):    {t_orig:.3f}s")
    print(f"  optimized (col counts):  {t_opt:.3f}s")
    print(f"  winner: {'optimized' if t_opt < t_orig else 'original'}  "
          f"({max(t_orig, t_opt) / min(t_orig, t_opt):.2f}x)")

    print()
    print("Sparse case (n=5, max_val=1000):")
    t_orig2 = timeit.timeit(lambda: orig(list(sparse)), number=n)
    t_opt2 = timeit.timeit(lambda: bead_sort(list(sparse)), number=n)
    print(f"  original (n² passes):    {t_orig2:.3f}s")
    print(f"  optimized (col counts):  {t_opt2:.3f}s")
    print(f"  winner: {'optimized' if t_opt2 < t_orig2 else 'original'}  "
          f"({max(t_orig2, t_opt2) / min(t_orig2, t_opt2):.2f}x)")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
