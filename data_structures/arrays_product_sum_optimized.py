"""
Optimized variants of Product Sum from a Special Array.

The product sum multiplies each element by its depth level.
For [x, [y, [z]]] = x*1 + y*2 + z*3.

Benchmarks three approaches using timeit.
"""

import timeit
from functools import reduce


# Variant 1: Original recursive approach
def product_sum_recursive(arr: list, depth: int = 1) -> int:
    """
    Recursive approach multiplying by depth.
    Time: O(n), Space: O(d) where d is max depth

    >>> product_sum_recursive([1, 2, 3])
    6
    >>> product_sum_recursive([1, [2, 3]])
    11
    >>> product_sum_recursive([1, [2, [3, 4]]])
    47
    """
    total = 0
    for ele in arr:
        total += product_sum_recursive(ele, depth + 1) if isinstance(ele, list) else ele
    return total * depth


# Variant 2: Iterative using explicit stack
def product_sum_iterative(arr: list) -> int:
    """
    Iterative using stack — avoids recursion overhead.
    Time: O(n), Space: O(d)

    >>> product_sum_iterative([1, 2, 3])
    6
    >>> product_sum_iterative([1, [2, 3]])
    11
    >>> product_sum_iterative([1, [2, [3, 4]]])
    47
    """
    stack = [(arr, 1)]
    total = 0
    while stack:
        current, depth = stack.pop()
        for ele in current:
            if isinstance(ele, list):
                stack.append((ele, depth + 1))
            else:
                total += ele * depth
    return total


# Variant 3: Generator-based flattening with depth tracking
def product_sum_generator(arr: list, depth: int = 1):
    """
    Generator that yields (value, depth) pairs; sum externally.
    Time: O(n), Space: O(d)

    >>> sum(v * d for v, d in product_sum_generator([1, 2, 3]))
    6
    >>> sum(v * d for v, d in product_sum_generator([1, [2, 3]]))
    11
    >>> sum(v * d for v, d in product_sum_generator([1, [2, [3, 4]]]))
    47
    """
    for ele in arr:
        if isinstance(ele, list):
            yield from product_sum_generator(ele, depth + 1)
        else:
            yield ele, depth


def benchmark():
    nested = [1, [2, [3, [4, [5, [6, [7, [8, [9, [10]]]]]]]]]]
    flat = list(range(1000))
    n = 10000

    t1 = timeit.timeit(lambda: product_sum_recursive(flat), number=n)
    t2 = timeit.timeit(lambda: product_sum_iterative(flat), number=n)
    t3 = timeit.timeit(lambda: sum(v * d for v, d in product_sum_generator(flat)), number=n)

    print(f"recursive:  {t1:.4f}s for {n} runs (flat list)")
    print(f"iterative:  {t2:.4f}s for {n} runs (flat list)")
    print(f"generator:  {t3:.4f}s for {n} runs (flat list)")

    t4 = timeit.timeit(lambda: product_sum_recursive(nested), number=n)
    t5 = timeit.timeit(lambda: product_sum_iterative(nested), number=n)
    t6 = timeit.timeit(lambda: sum(v * d for v, d in product_sum_generator(nested)), number=n)

    print(f"recursive:  {t4:.4f}s for {n} runs (deeply nested)")
    print(f"iterative:  {t5:.4f}s for {n} runs (deeply nested)")
    print(f"generator:  {t6:.4f}s for {n} runs (deeply nested)")


if __name__ == "__main__":
    benchmark()
