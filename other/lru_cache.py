"""
LRU Cache — Using Python's functools.lru_cache and OrderedDict.

Demonstrates both the standard library approach and a manual OrderedDict
implementation of LRU caching.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/lru_cache.py
"""

from __future__ import annotations

from collections import OrderedDict


class LRUCache:
    """
    LRU Cache using OrderedDict for O(1) operations.

    >>> cache = LRUCache(2)
    >>> cache.put(1, 1)
    >>> cache.put(2, 2)
    >>> cache.get(1)
    1
    >>> cache.put(3, 3)
    >>> cache.get(2)
    -1
    >>> cache.get(3)
    3
    >>> cache.put(4, 4)
    >>> cache.get(1)
    -1
    >>> cache.get(3)
    3
    >>> cache.get(4)
    4
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        """Get value, moving key to most recent. Returns -1 if not found."""
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """Insert or update, evicting LRU if over capacity."""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def lru_cache_demo() -> None:
    """
    Demonstrate functools.lru_cache for memoization.

    >>> lru_cache_demo()
    fib(10) = 55
    fib(20) = 6765
    """
    from functools import lru_cache

    @lru_cache(maxsize=128)
    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)

    print(f"fib(10) = {fib(10)}")
    print(f"fib(20) = {fib(20)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
