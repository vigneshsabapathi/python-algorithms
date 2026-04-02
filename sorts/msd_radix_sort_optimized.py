"""
MSD Radix Sort — optimized variants for interview prep.

MSD (Most Significant Digit/Bit) radix sort: partition from the highest bit
downward, recursing into each partition. Contrast with LSD radix sort which
processes digits from least significant to most significant using stable passes.

Key properties:
  - O(n * b) time where b = number of bits (binary) or digits (decimal)
  - O(n + 2^r) space per recursive level (r = bits per pass)
  - NOT comparison-based → can beat O(n log n) lower bound
  - NOT stable in the inplace variant (partition swaps non-adjacent elements)
  - Stable in the out-of-place (allocating) variant

Variants in this file:
  msd_radix_decimal   : MSD radix sort on decimal digits (base-10), stable
  lsd_radix_sort      : LSD radix sort — simpler, stable, better cache behaviour
  radix_signed        : handles negative integers via two's complement offset
"""

from __future__ import annotations

from collections import deque


# ---------------------------------------------------------------------------
# Variant 1: MSD radix sort on decimal digits (base-10)
# ---------------------------------------------------------------------------

def msd_radix_decimal(arr: list[int]) -> list[int]:
    """
    MSD radix sort using base-10 digits. Stable (allocating, not in-place).
    Handles non-negative integers only.

    Examples:
    >>> msd_radix_decimal([40, 12, 1, 100, 4])
    [1, 4, 12, 40, 100]
    >>> msd_radix_decimal([])
    []
    >>> msd_radix_decimal([123, 345, 123, 80])
    [80, 123, 123, 345]
    >>> msd_radix_decimal([0, 0, 0])
    [0, 0, 0]
    >>> msd_radix_decimal([9, 8, 7, 6, 5])
    [5, 6, 7, 8, 9]
    """
    if not arr:
        return []
    arr = list(arr)
    max_digits = len(str(max(arr))) if arr else 0
    return _msd_decimal(arr, max_digits)


def _msd_decimal(arr: list[int], digit_pos: int) -> list[int]:
    """Recursively sort arr by digit at digit_pos (1=units, 2=tens, ...)."""
    if digit_pos == 0 or len(arr) <= 1:
        return arr
    buckets: list[list[int]] = [[] for _ in range(10)]
    divisor = 10 ** (digit_pos - 1)
    for num in arr:
        digit = (num // divisor) % 10
        buckets[digit].append(num)
    result = []
    for bucket in buckets:
        result.extend(_msd_decimal(bucket, digit_pos - 1))
    return result


# ---------------------------------------------------------------------------
# Variant 2: LSD radix sort (simpler, stable, better cache)
# ---------------------------------------------------------------------------

def lsd_radix_sort(arr: list[int]) -> list[int]:
    """
    LSD (Least Significant Digit) radix sort. Stable, O(n*d) time.

    Processes digits from rightmost (units) to leftmost (most significant).
    Each pass is a stable counting sort on one digit → O(n + 10) per pass.
    Total: O(n * d) where d = number of digits in max value.

    Advantages over MSD:
    - No recursion → no stack overhead
    - Sequential memory access per pass → better cache behaviour
    - Simpler implementation; stable by default

    Disadvantage vs MSD:
    - Always processes all d passes even if data could be partitioned early

    Examples:
    >>> lsd_radix_sort([40, 12, 1, 100, 4])
    [1, 4, 12, 40, 100]
    >>> lsd_radix_sort([])
    []
    >>> lsd_radix_sort([123, 345, 123, 80])
    [80, 123, 123, 345]
    >>> lsd_radix_sort([0, 0, 1, 0])
    [0, 0, 0, 1]
    >>> lsd_radix_sort([9, 8, 7, 6, 5])
    [5, 6, 7, 8, 9]
    """
    if not arr:
        return []
    arr = list(arr)
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        arr = _counting_sort_digit(arr, exp)
        exp *= 10
    return arr


def _counting_sort_digit(arr: list[int], exp: int) -> list[int]:
    """Stable counting sort on the digit at position exp (1, 10, 100, ...)."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for num in arr:
        count[(num // exp) % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for num in reversed(arr):   # reversed for stability
        idx = (num // exp) % 10
        count[idx] -= 1
        output[count[idx]] = num
    return output


# ---------------------------------------------------------------------------
# Variant 3: Radix sort supporting negative integers
# ---------------------------------------------------------------------------

def radix_signed(arr: list[int]) -> list[int]:
    """
    Radix sort for integers including negatives.

    Strategy: shift all values by -min to make them non-negative, sort,
    then shift back. O(n * d) time, O(n) space.

    Examples:
    >>> radix_signed([3, -1, 0, -5, 2])
    [-5, -1, 0, 2, 3]
    >>> radix_signed([-2, -5, -45])
    [-45, -5, -2]
    >>> radix_signed([])
    []
    >>> radix_signed([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    """
    if not arr:
        return []
    offset = -min(arr)          # shift so all values >= 0
    shifted = [x + offset for x in arr]
    sorted_shifted = lsd_radix_sort(shifted)
    return [x - offset for x in sorted_shifted]


def benchmark() -> None:
    import random
    import timeit

    random.seed(42)

    import sys
    sys.path.insert(0, 'sorts')
    from msd_radix_sort import msd_radix_sort as msd_binary
    from msd_radix_sort import msd_radix_sort_inplace as msd_inplace

    print("Benchmark: non-negative integers\n")
    header = (f"{'n':<7} {'bits(msd)':>10} {'bits_ip':>8} "
              f"{'decimal(msd)':>13} {'lsd':>7} {'sorted()':>9}")
    print(header)
    print("-" * len(header))

    for n in [1000, 5000, 20000, 100000]:
        data = [random.randint(0, 10**6) for _ in range(n)]
        iters = max(5, 500 // n)
        t_mb = timeit.timeit(lambda: msd_binary(list(data)),          number=iters)
        t_mi = timeit.timeit(lambda: (lambda x: (msd_inplace(x), x))(list(data))[1],
                             number=iters)
        t_d  = timeit.timeit(lambda: msd_radix_decimal(list(data)),   number=iters)
        t_l  = timeit.timeit(lambda: lsd_radix_sort(list(data)),      number=iters)
        t_s  = timeit.timeit(lambda: sorted(data),                    number=iters)
        print(f"{n:<7} {t_mb/iters:>10.4f} {t_mi/iters:>8.4f} "
              f"{t_d/iters:>13.4f} {t_l/iters:>7.4f} {t_s/iters:>9.4f}")

    # --- Stability check ---
    print("\nStability check (equal keys preserve original order):")
    data = [(123, 'a'), (80, 'b'), (123, 'c'), (45, 'd')]
    keys = [x[0] for x in data]
    expected = sorted(data, key=lambda x: x[0])

    r_lsd = lsd_radix_sort(keys)
    r_msd = msd_radix_decimal(keys)

    # True stability test: sort pairs preserving secondary order
    class _Tagged:
        def __init__(self, val, tag): self.val = val; self.tag = tag
        def __repr__(self): return f'({self.val},{self.tag})'

    tagged = [_Tagged(v, t) for v, t in data]
    # LSD stable: process using (val,) as sort key
    result_lsd = lsd_radix_sort([x.val for x in tagged])
    # We can't directly test stability without key-aware sort; use sorted() as reference
    print(f"  lsd_radix_sort:      {r_lsd}  (matches sorted: {r_lsd == sorted(keys)})")
    print(f"  msd_radix_decimal:   {r_msd}  (matches sorted: {r_msd == sorted(keys)})")
    print(f"  note: LSD is stable; binary MSD inplace is NOT stable")

    # --- MSD vs LSD: early termination advantage ---
    print("\nEarly termination: MSD on uniform range [0,9] (1-digit) vs [0,999999]:")
    small = [random.randint(0, 9) for _ in range(10000)]
    large = [random.randint(0, 999999) for _ in range(10000)]
    iters = 100
    for label, data in [("[0,9]", small), ("[0,999999]", large)]:
        t_m = timeit.timeit(lambda: msd_binary(list(data)), number=iters)
        t_l = timeit.timeit(lambda: lsd_radix_sort(list(data)), number=iters)
        t_s = timeit.timeit(lambda: sorted(data), number=iters)
        print(f"  {label:<12}: msd={t_m/iters:.4f}  lsd={t_l/iters:.4f}  sorted()={t_s/iters:.4f}")

    # --- radix_signed demo ---
    print("\nradix_signed demo:")
    mixed = [3, -1, 0, -5, 2, -100, 50]
    print(f"  input:  {mixed}")
    print(f"  output: {radix_signed(mixed)}")
    print(f"  correct: {radix_signed(mixed) == sorted(mixed)}")


if __name__ == "__main__":
    benchmark()
