"""
Merge-Insertion Sort (Ford-Johnson Algorithm) — optimized variants for interview prep.

Merge-insertion sort (Ford-Johnson, 1959) is historically important because it
achieves the theoretical minimum number of comparisons to sort n elements for
small n. It's NOT practical — the overhead of pairing, recursive sorting, and
binary search insertions makes it slower than std sorts in wall-clock time.

The algorithm:
  1. Pair elements; sort each pair (1 comparison each)
  2. Sort the "larger" elements of each pair recursively (n/2 elements, recursive)
  3. The smallest "smaller" element is the global min → place at front
  4. Insert remaining "smaller" elements in Jacobsthal order using binary search

The OPTIMAL insertion order uses Jacobsthal numbers:
  J(0)=0, J(1)=1, J(n)=J(n-1)+2*J(n-2)  →  [0,1,1,3,5,11,21,43,85,...]

  In 1-indexed b terms, insert in groups:
    b_3, b_2         (group ending at J(3)=3)
    b_5, b_4         (group ending at J(4)=5)
    b_11,...,b_6     (group ending at J(5)=11)
    ...

  Each group of size t_k = J(k)-J(k-1) can be inserted with ≤ k-1 comparisons each.
  This minimises the worst-case total comparison count.

The original implementation uses a SIMPLIFIED sequential insertion order
(i=0,1,2,...) which is correct but uses more comparisons than optimal.

Variants:
  merge_insertion_sort_jacobsthal : true Ford-Johnson with Jacobsthal insertion order
  comparison_counter              : instruments comparison counts
  merge_sort_reference            : standard merge sort (faster in practice)
"""

from __future__ import annotations

import bisect


# ---------------------------------------------------------------------------
# Jacobsthal sequence
# ---------------------------------------------------------------------------

def _jacobsthal(n: int) -> int:
    """Return the nth Jacobsthal number: J(0)=0, J(1)=1, J(n)=J(n-1)+2*J(n-2)."""
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, b + 2 * a
    return b


def _jacobsthal_insertion_order(n: int) -> list[int]:
    """
    Return the 0-indexed Jacobsthal insertion order for n pending elements.

    pending[i] corresponds to b_{i+2} in the 1-indexed Ford-Johnson scheme
    (b_1 is already placed; pending starts at b_2).

    Standard 1-indexed insertion order: b_3, b_2, b_5, b_4, b_11,...,b_6, ...
    Converted to 0-indexed pending: b_{i+2} → index i.

    >>> _jacobsthal_insertion_order(0)
    []
    >>> _jacobsthal_insertion_order(1)
    [0]
    >>> _jacobsthal_insertion_order(5)
    [1, 0, 3, 2, 4]
    >>> _jacobsthal_insertion_order(8)
    [1, 0, 3, 2, 7, 6, 5, 4]
    """
    if n == 0:
        return []
    order = []
    k = 3
    while True:
        jk   = _jacobsthal(k)      # upper end of group (1-indexed b position)
        jkm1 = _jacobsthal(k - 1)  # lower end + 1 (exclusive lower bound)
        # 1-indexed b positions: jk, jk-1, ..., jkm1+1
        # 0-indexed pending:      jk-2, jk-3, ..., jkm1-1
        hi_0 = min(jk, n + 1) - 2      # inclusive upper, capped at n-1
        lo_0 = jkm1 - 1                 # inclusive lower
        if lo_0 >= n:
            break
        for idx in range(hi_0, lo_0 - 1, -1):
            if 0 <= idx < n:
                order.append(idx)
        if jk >= n + 1:
            break
        k += 1
    return order


# ---------------------------------------------------------------------------
# Helper: merge-sort pairs by their first element
# ---------------------------------------------------------------------------

def _sort_by_first(pairs: list[tuple]) -> list[tuple]:
    """Stable merge sort on list of tuples, ordered by first element."""
    if len(pairs) <= 1:
        return pairs
    mid = len(pairs) // 2
    left  = _sort_by_first(pairs[:mid])
    right = _sort_by_first(pairs[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][0] <= right[j][0]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]


# ---------------------------------------------------------------------------
# Variant 1: Ford-Johnson with Jacobsthal insertion order
# ---------------------------------------------------------------------------

def merge_insertion_sort_jacobsthal(collection: list) -> list:
    """
    Ford-Johnson merge-insertion sort with Jacobsthal insertion order.

    Uses the theoretically optimal number of comparisons for small n.
    Not practical for large n due to overhead — use sorted() in production.

    Examples:
    >>> merge_insertion_sort_jacobsthal([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> merge_insertion_sort_jacobsthal([])
    []
    >>> merge_insertion_sort_jacobsthal([99])
    [99]
    >>> merge_insertion_sort_jacobsthal([-2, -5, -45])
    [-45, -5, -2]
    >>> merge_insertion_sort_jacobsthal([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> merge_insertion_sort_jacobsthal([999, 100, 75, 40, 10000])
    [40, 75, 100, 999, 10000]

    All permutations of 0..5:
    >>> import itertools
    >>> all(merge_insertion_sort_jacobsthal(list(p)) == sorted(p)
    ...     for p in itertools.permutations(range(6)))
    True
    """
    arr = list(collection)
    n = len(arr)
    if n <= 1:
        return arr

    # Step 1: pair elements, sort each pair → (larger=a_i, smaller=b_i)
    pairs = []
    for i in range(0, n - 1, 2):
        if arr[i] <= arr[i + 1]:
            pairs.append((arr[i + 1], arr[i]))   # (a_i, b_i), a_i >= b_i
        else:
            pairs.append((arr[i], arr[i + 1]))
    odd = arr[-1] if n % 2 == 1 else None

    # Step 2: sort pairs by their a_i (larger element) → a_1 <= a_2 <= ...
    sorted_pairs = _sort_by_first(pairs)

    # Step 3: chain = [b_1, a_1, a_2, ..., a_k]
    # b_1 is guaranteed smallest: b_1 <= a_1 (paired), a_1 <= a_2 <= ... (sorted)
    chain: list = [sorted_pairs[0][1]]      # b_1
    for p in sorted_pairs:
        chain.append(p[0])                  # a_1, a_2, ...

    # Step 4: pending = [b_2, b_3, ..., b_k] + optional odd
    pending = [p[1] for p in sorted_pairs[1:]]
    if odd is not None:
        pending.append(odd)

    # Step 5: insert pending in Jacobsthal order
    # For pending[i] (= b_{i+2}): upper bound is a_{i+2} = sorted_pairs[i+1][0]
    # since b_{i+2} <= a_{i+2} by pairing construction.
    order = _jacobsthal_insertion_order(len(pending))
    for idx in order:
        val = pending[idx]
        if idx < len(sorted_pairs) - 1:
            # Known upper bound: paired a_{idx+2}
            upper_val = sorted_pairs[idx + 1][0]
            hi = bisect.bisect_right(chain, upper_val)
            pos = bisect.bisect_left(chain, val, 0, hi)
        else:
            # Odd element (no paired a) → search entire chain
            pos = bisect.bisect_left(chain, val)
        chain.insert(pos, val)

    return chain


# ---------------------------------------------------------------------------
# Variant 2: Comparison counter
# ---------------------------------------------------------------------------

class _CompCount:
    """Wraps a value and counts every comparison."""
    def __init__(self, val, counter: list):
        self.val = val
        self.counter = counter

    def __lt__(self, other):  self.counter[0] += 1; return self.val < other.val
    def __le__(self, other):  self.counter[0] += 1; return self.val <= other.val
    def __gt__(self, other):  self.counter[0] += 1; return self.val > other.val
    def __ge__(self, other):  self.counter[0] += 1; return self.val >= other.val
    def __eq__(self, other):  self.counter[0] += 1; return self.val == other.val
    def __repr__(self):       return repr(self.val)


def count_comparisons(sort_fn, data: list) -> tuple[list, int]:
    """Run sort_fn on wrapped data, counting all comparisons."""
    counter = [0]
    wrapped = [_CompCount(v, counter) for v in data]
    result = sort_fn(wrapped)
    unwrapped = [x.val for x in result]
    return unwrapped, counter[0]


# ---------------------------------------------------------------------------
# Reference: standard merge sort
# ---------------------------------------------------------------------------

def merge_sort(arr: list) -> list:
    """Standard recursive merge sort — O(n log n) comparisons, fast in practice.

    Examples:
    >>> merge_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> merge_sort([])
    []
    >>> merge_sort([4, 3, 2, 1])
    [1, 2, 3, 4]
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]


def benchmark() -> None:
    import random
    import timeit

    random.seed(42)

    import sys
    sys.path.insert(0, 'sorts')
    from merge_insertion_sort import merge_insertion_sort as original

    # --- Comparison count analysis ---
    # Known Ford-Johnson optimal worst-case values:
    # n:  1  2  3  4  5   6   7   8   9  10  11  12
    # W:  0  1  3  5  7  10  13  16  19  22  26  30
    ford_johnson_optimal = {1:0, 2:1, 3:3, 4:5, 5:7, 6:10, 7:13, 8:16,
                            9:19, 10:22, 11:26, 12:30}

    print("=== Comparison counts (worst-case: reversed input) ===\n")
    header = (f"{'n':<5} {'FJ_optimal':>11} {'original':>10} "
              f"{'jacobsthal':>12} {'merge_sort':>11} {'sorted()':>9}")
    print(header)
    print("-" * len(header))

    for n in range(2, 13):
        data = list(range(n, 0, -1))
        _, c_orig = count_comparisons(lambda x: original(list(x)), data)
        _, c_jac  = count_comparisons(merge_insertion_sort_jacobsthal, data)
        _, c_ms   = count_comparisons(merge_sort, data)
        _, c_py   = count_comparisons(sorted, data)
        opt = ford_johnson_optimal.get(n, '?')
        print(f"{n:<5} {str(opt):>11} {c_orig:>10} {c_jac:>12} {c_ms:>11} {c_py:>9}")

    # --- Wall-clock benchmark ---
    print("\n=== Wall-clock benchmark (random data) ===\n")
    header2 = (f"{'n':<7} {'iters':>6} {'original':>10} {'jacobsthal':>12} "
               f"{'merge_sort':>11} {'sorted()':>9}")
    print(header2)
    print("-" * len(header2))

    for n in [10, 50, 100, 500, 1000]:
        data = [random.randint(0, 9999) for _ in range(n)]
        iters = max(10, 1000 // n)
        t_o = timeit.timeit(lambda: original(list(data)),                          number=iters)
        t_j = timeit.timeit(lambda: merge_insertion_sort_jacobsthal(list(data)),   number=iters)
        t_m = timeit.timeit(lambda: merge_sort(list(data)),                        number=iters)
        t_s = timeit.timeit(lambda: sorted(data),                                  number=iters)
        print(f"{n:<7} {iters:>6} {t_o:>10.4f} {t_j:>12.4f} {t_m:>11.4f} {t_s:>9.4f}")

    # --- Stability check ---
    print("\n=== Stability check ===")
    data = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd'), (3, 'e')]
    expected = sorted(data, key=lambda x: x[0])
    r_orig = original(list(data))
    r_jac  = merge_insertion_sort_jacobsthal(list(data))
    print(f"  Input:      {data}")
    print(f"  Expected:   {expected}")
    print(f"  original:   {r_orig}  stable={r_orig == expected}")
    print(f"  jacobsthal: {r_jac}  stable={r_jac == expected}")


if __name__ == "__main__":
    benchmark()
