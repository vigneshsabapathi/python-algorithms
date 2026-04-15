"""k-th lexicographic permutation — variants + benchmark."""

import time
from math import factorial
from itertools import islice, permutations


def kth_factorial_base(n, k):
    digits = list(range(n))
    result = []
    for i in range(n, 0, -1):
        f = factorial(i - 1)
        idx = k // f
        k %= f
        result.append(digits.pop(idx))
    return result


def kth_itertools(n, k):
    return list(next(islice(permutations(range(n)), k, k + 1)))


def kth_next_permutation(n, k):
    """Start from identity, call next_permutation k times."""
    arr = list(range(n))
    for _ in range(k):
        # next_permutation
        i = len(arr) - 2
        while i >= 0 and arr[i] >= arr[i + 1]:
            i -= 1
        if i < 0:
            break
        j = len(arr) - 1
        while arr[j] <= arr[i]:
            j -= 1
        arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1 :] = arr[i + 1 :][::-1]
    return arr


def benchmark():
    n = 10
    k = factorial(n) // 2
    for name, fn in [
        ("factorial_base_O(n2)", kth_factorial_base),
        ("itertools_islice", kth_itertools),
        ("next_permutation_kx", kth_next_permutation),
    ]:
        start = time.perf_counter()
        r = fn(n, k)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:22s} perm[0:5]={r[:5]}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
