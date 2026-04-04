"""Tree Sort — optimized and alternative implementations.

Four approaches compared:
  1. Recursive BST (baseline) — drops duplicates, O(n²) worst case on sorted input
  2. Recursive BST with duplicate support — stores count per node
  3. Iterative BST insert — no recursion limit risk for large inputs
  4. sortedcontainers.SortedList — C-backed balanced BST, O(n log n) guaranteed

Problem with baseline:
  - Equal values are silently skipped in insert(), so duplicates vanish.
  - A pre-sorted or reverse-sorted input degenerates the BST into a linked list
    causing O(n²) time and O(n) stack depth (recursion limit risk).

References:
  Binary Search Tree: https://en.wikipedia.org/wiki/Binary_search_tree
  AVL / self-balancing: https://en.wikipedia.org/wiki/AVL_tree
  sortedcontainers: https://grantjenks.com/docs/sortedcontainers/
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Approach 1: Recursive BST — baseline (drops duplicates)
# ---------------------------------------------------------------------------

@dataclass
class NodeBasic:
    val: int
    left: NodeBasic | None = None
    right: NodeBasic | None = None

    def __iter__(self) -> Iterator[int]:
        if self.left:
            yield from self.left
        yield self.val
        if self.right:
            yield from self.right

    def insert(self, val: int) -> None:
        if val < self.val:
            if self.left is None:
                self.left = NodeBasic(val)
            else:
                self.left.insert(val)
        elif val > self.val:
            if self.right is None:
                self.right = NodeBasic(val)
            else:
                self.right.insert(val)
        # equal: silently skipped → duplicates dropped


def tree_sort_recursive(arr: list[int]) -> list[int]:
    """Recursive BST tree sort — duplicates dropped.

    Examples:
        >>> tree_sort_recursive([5, 2, 7, 1])
        [1, 2, 5, 7]
        >>> tree_sort_recursive([])
        []
        >>> tree_sort_recursive([3, 1, 3, 2])  # duplicate 3 dropped
        [1, 2, 3]
    """
    if not arr:
        return []
    root = NodeBasic(arr[0])
    for item in arr[1:]:
        root.insert(item)
    return list(root)


# ---------------------------------------------------------------------------
# Approach 2: Recursive BST with duplicate support (count per node)
# ---------------------------------------------------------------------------

@dataclass
class NodeWithCount:
    val: int
    count: int = 1
    left: NodeWithCount | None = None
    right: NodeWithCount | None = None

    def __iter__(self) -> Iterator[int]:
        if self.left:
            yield from self.left
        yield from (self.val for _ in range(self.count))
        if self.right:
            yield from self.right

    def insert(self, val: int) -> None:
        if val < self.val:
            if self.left is None:
                self.left = NodeWithCount(val)
            else:
                self.left.insert(val)
        elif val > self.val:
            if self.right is None:
                self.right = NodeWithCount(val)
            else:
                self.right.insert(val)
        else:
            self.count += 1  # duplicate: increment count


def tree_sort_with_duplicates(arr: list[int]) -> list[int]:
    """Recursive BST tree sort — preserves duplicates via per-node count.

    Examples:
        >>> tree_sort_with_duplicates([5, 2, 7, 1])
        [1, 2, 5, 7]
        >>> tree_sort_with_duplicates([])
        []
        >>> tree_sort_with_duplicates([3, 1, 3, 2])  # duplicate 3 preserved
        [1, 2, 3, 3]
        >>> tree_sort_with_duplicates([4, 4, 4])
        [4, 4, 4]
    """
    if not arr:
        return []
    root = NodeWithCount(arr[0])
    for item in arr[1:]:
        root.insert(item)
    return list(root)


# ---------------------------------------------------------------------------
# Approach 3: Iterative BST insert (no recursion limit risk)
# ---------------------------------------------------------------------------

@dataclass
class NodeIter:
    val: int
    count: int = 1
    left: NodeIter | None = None
    right: NodeIter | None = None

    def __iter__(self) -> Iterator[int]:
        if self.left:
            yield from self.left
        yield from (self.val for _ in range(self.count))
        if self.right:
            yield from self.right


def _insert_iterative(root: NodeIter, val: int) -> None:
    """Insert val into BST rooted at root using an explicit loop."""
    current = root
    while True:
        if val < current.val:
            if current.left is None:
                current.left = NodeIter(val)
                return
            current = current.left
        elif val > current.val:
            if current.right is None:
                current.right = NodeIter(val)
                return
            current = current.right
        else:
            current.count += 1
            return


def tree_sort_iterative(arr: list[int]) -> list[int]:
    """Iterative BST tree sort — safe for large inputs, preserves duplicates.

    Avoids Python recursion limit by using an explicit while-loop for insert.
    In-order traversal (the __iter__) is still recursive — for production use
    on very deep trees, replace with an iterative in-order traversal as well.

    Examples:
        >>> tree_sort_iterative([5, 2, 7, 1])
        [1, 2, 5, 7]
        >>> tree_sort_iterative([])
        []
        >>> tree_sort_iterative([3, 1, 3, 2])
        [1, 2, 3, 3]
        >>> tree_sort_iterative([4, 4, 4])
        [4, 4, 4]
    """
    if not arr:
        return []
    root = NodeIter(arr[0])
    for item in arr[1:]:
        _insert_iterative(root, item)
    return list(root)


# ---------------------------------------------------------------------------
# Approach 4: sortedcontainers.SortedList
# ---------------------------------------------------------------------------

def tree_sort_sortedcontainers(arr: list[int]) -> list[int]:
    """Sort using sortedcontainers.SortedList — C-backed, O(n log n) guaranteed.

    SortedList maintains sorted order on every insertion using a B-tree
    variant internally.  Much faster than a naive BST for large inputs and
    does not degenerate on sorted/reverse-sorted data.

    Requires: pip install sortedcontainers

    Examples:
        >>> tree_sort_sortedcontainers([5, 2, 7, 1])
        [1, 2, 5, 7]
        >>> tree_sort_sortedcontainers([])
        []
        >>> tree_sort_sortedcontainers([3, 1, 3, 2])
        [1, 2, 3, 3]
        >>> tree_sort_sortedcontainers([4, 4, 4])
        [4, 4, 4]
    """
    from sortedcontainers import SortedList  # type: ignore[import]

    sl = SortedList(arr)
    return list(sl)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare all four approaches on random, sorted, and reverse-sorted inputs."""
    import random
    import timeit

    random.seed(42)
    n = 2000
    random_data = [random.randint(-1000, 1000) for _ in range(n)]
    sorted_data = list(range(n))           # worst case for naive BST
    reverse_data = list(range(n, 0, -1))   # worst case for naive BST

    datasets = {
        f"random     ({n} items)": random_data,
        f"sorted     ({n} items)": sorted_data,
        f"reverse    ({n} items)": reverse_data,
    }

    implementations = {
        "recursive BST (no dups)":   tree_sort_recursive,
        "recursive BST (with dups)": tree_sort_with_duplicates,
        "iterative BST":             tree_sort_iterative,
        "sortedcontainers":          tree_sort_sortedcontainers,
    }

    runs = 200

    print(f"\nBenchmark — Tree Sort variants ({runs} runs each)\n")

    for ds_name, data in datasets.items():
        print(f"  Dataset: {ds_name}")
        print(f"  {'Implementation':<30} {'Time (ms)':>12}")
        print("  " + "-" * 45)
        results: dict[str, float] = {}
        for name, fn in implementations.items():
            # sorted baseline degenerates (skip to avoid hanging)
            if "no dups" in name and "sorted" in ds_name:
                print(f"  {'recursive BST (no dups)':<30} {'SKIP (degenerate)':>12}")
                continue
            if "no dups" in name and "reverse" in ds_name:
                print(f"  {'recursive BST (no dups)':<30} {'SKIP (degenerate)':>12}")
                continue
            try:
                t = timeit.timeit(lambda fn=fn, data=data: fn(data), number=runs)
                results[name] = t
                print(f"  {name:<30} {t * 1000:>12.2f}")
            except RecursionError:
                print(f"  {name:<30} {'RecursionError':>12}")
        print()

    # Correctness check
    sample = [5, 3, 8, 1, 5, 2, 9, 3]
    print("Correctness on [5, 3, 8, 1, 5, 2, 9, 3]:")
    print(f"  recursive BST (no dups):   {tree_sort_recursive(sample)}")
    print(f"  recursive BST (with dups): {tree_sort_with_duplicates(sample)}")
    print(f"  iterative BST:             {tree_sort_iterative(sample)}")
    print(f"  sortedcontainers:          {tree_sort_sortedcontainers(sample)}")
    print(f"  expected (sorted()):       {sorted(sample)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    benchmark()
