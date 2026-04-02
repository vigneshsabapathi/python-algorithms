"""
Gnome Sort — optimized variants for interview prep.

Original gnome sort: O(n^2) time, O(1) space. Like insertion sort but moves
elements backward via swaps rather than shifts. Named after garden gnomes
sorting flower pots — look left, if out of order swap and step back, else step forward.

Key insight: gnome sort is insertion sort with swaps instead of shifts.
The "teleport" optimization avoids the wasted forward traversal.

Variants:
  gnome_sort_teleport:  teleporting gnome — jumps back to insertion frontier
  insertion_sort:       standard insertion sort using shifts (O(n^2) but fewer writes)
  insertion_sort_binary: binary search to find position, then shift
                         (O(n log n) comparisons — good for expensive comparisons)
"""

from __future__ import annotations

import bisect


def gnome_sort_teleport(lst: list) -> list:
    """
    Teleporting gnome sort: stores position before stepping back, jumps
    forward after insertion rather than stepping one at a time.

    Without teleport: gnome walks backward to insertion point, then forward
    again to the frontier — O(n^2) forward steps wasted.
    With teleport: O(n) forward steps total (bookmark tracks the frontier).

    Examples:
    >>> gnome_sort_teleport([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> gnome_sort_teleport([])
    []

    >>> gnome_sort_teleport([-2, -5, -45])
    [-45, -5, -2]

    >>> gnome_sort_teleport([4, 3, 2, 1])
    [1, 2, 3, 4]

    >>> gnome_sort_teleport([1, 2, 3, 4])
    [1, 2, 3, 4]
    """
    if len(lst) <= 1:
        return lst

    i = 1
    bookmark = 2  # next frontier position to jump to after insertion

    while i < len(lst):
        if lst[i - 1] <= lst[i]:
            i += 1
        else:
            lst[i - 1], lst[i] = lst[i], lst[i - 1]
            i -= 1
            if i == 0:
                # Finished inserting: teleport to frontier
                i = bookmark
                bookmark += 1

    return lst


def insertion_sort(lst: list) -> list:
    """
    Standard insertion sort: shifts elements right to make room, then places.
    O(n^2) time, O(1) space. Adaptive: O(n) on nearly-sorted input.

    Fewer writes than gnome sort: each element shifted once per position
    (1 write), vs gnome sort which swaps at every step (2 writes per step).
    Stable: equal elements keep their relative order.

    Examples:
    >>> insertion_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> insertion_sort([])
    []

    >>> insertion_sort([-2, -5, -45])
    [-45, -5, -2]

    >>> insertion_sort([4, 3, 2, 1])
    [1, 2, 3, 4]

    >>> insertion_sort([1, 2, 3, 4])
    [1, 2, 3, 4]
    """
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and lst[j] > key:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
    return lst


def insertion_sort_binary(lst: list) -> list:
    """
    Binary insertion sort: uses bisect to find insertion position in O(log n)
    comparisons, then shifts. Total: O(n log n) comparisons, O(n^2) shifts.

    Best when comparisons are expensive (custom __lt__, remote calls).
    For simple int/str, the shift cost dominates — no wall-clock improvement.
    Stable: bisect_left ensures equal elements maintain their order.

    Examples:
    >>> insertion_sort_binary([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> insertion_sort_binary([])
    []

    >>> insertion_sort_binary([-2, -5, -45])
    [-45, -5, -2]

    >>> insertion_sort_binary([4, 3, 2, 1])
    [1, 2, 3, 4]

    >>> insertion_sort_binary([1, 2, 3, 4])
    [1, 2, 3, 4]
    """
    for i in range(1, len(lst)):
        key = lst[i]
        pos = bisect.bisect_left(lst, key, 0, i)
        lst[pos + 1 : i + 1] = lst[pos:i]
        lst[pos] = key
    return lst


def _gnome_original(lst: list) -> list:
    """Reference: original gnome sort (no teleport)."""
    if len(lst) <= 1:
        return lst
    i = 1
    while i < len(lst):
        if lst[i - 1] <= lst[i]:
            i += 1
        else:
            lst[i - 1], lst[i] = lst[i], lst[i - 1]
            i -= 1
            if i == 0:
                i = 1
    return lst


def benchmark() -> None:
    import copy
    import random
    import timeit

    random.seed(42)
    n = 200
    iters = 2000

    datasets = {
        "random":       [random.randint(0, 999) for _ in range(n)],
        "reversed":     list(range(n, 0, -1)),
        "nearly sorted": list(range(n)) + [random.randint(0, n) for _ in range(5)],
        "sorted":       list(range(n)),
    }

    print(f"Benchmark: n={n}, {iters} iterations each\n")
    header = f"{'Dataset':<20} {'gnome':>8} {'gnome_tp':>9} {'insertion':>10} {'ins_bin':>8} {'sorted()':>9}"
    print(header)
    print("-" * len(header))

    for label, data in datasets.items():
        t_g  = timeit.timeit(lambda: _gnome_original(list(data)),        number=iters)
        t_gt = timeit.timeit(lambda: gnome_sort_teleport(list(data)),    number=iters)
        t_i  = timeit.timeit(lambda: insertion_sort(list(data)),         number=iters)
        t_ib = timeit.timeit(lambda: insertion_sort_binary(list(data)),  number=iters)
        t_s  = timeit.timeit(lambda: sorted(data),                       number=iters)
        print(f"{label:<20} {t_g:>8.3f} {t_gt:>9.3f} {t_i:>10.3f} {t_ib:>8.3f} {t_s:>9.3f}")

    # --- Write count comparison ---
    print(f"\nWrite counts, n=20 reversed [20..1]:")

    def gnome_write_count(data: list) -> tuple[list, int]:
        lst = list(data)
        count = 0
        if len(lst) <= 1:
            return lst, count
        i = 1
        while i < len(lst):
            if lst[i - 1] <= lst[i]:
                i += 1
            else:
                lst[i - 1], lst[i] = lst[i], lst[i - 1]
                count += 2  # swap = 2 assignments
                i -= 1
                if i == 0:
                    i = 1
        return lst, count

    def insertion_write_count(data: list) -> tuple[list, int]:
        lst = list(data)
        count = 0
        for i in range(1, len(lst)):
            key = lst[i]
            j = i - 1
            while j >= 0 and lst[j] > key:
                lst[j + 1] = lst[j]
                count += 1
                j -= 1
            lst[j + 1] = key
            count += 1  # placement
        return lst, count

    rev20 = list(range(20, 0, -1))
    _, gw = gnome_write_count(rev20)
    _, iw = insertion_write_count(rev20)
    print(f"  gnome sort:     {gw} writes (2 per swap)")
    print(f"  insertion sort: {iw} writes (1 shift + 1 place per element)")
    print(f"  ratio: gnome does {gw / iw:.1f}x more writes")

    # --- Stability check ---
    print("\nStability check (equal keys keep original order):")
    data_pairs = [(2, 'a'), (2, 'b'), (1, 'c')]
    r_gnome = _gnome_original(copy.copy(data_pairs))
    r_ins   = insertion_sort(copy.copy(data_pairs))
    expected = [(1, 'c'), (2, 'a'), (2, 'b')]
    print(f"  Input:            {data_pairs}")
    print(f"  gnome result:     {r_gnome}  stable={r_gnome == expected}")
    print(f"  insertion result: {r_ins}  stable={r_ins == expected}")


if __name__ == "__main__":
    benchmark()
