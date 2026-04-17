"""
Optimized variants of Hash Table with Open Addressing.

Three collision resolution strategies:
1. Linear probing (original)
2. Quadratic probing
3. Double hashing

Benchmarks using timeit.
"""

import math
import timeit


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if not n % 2:
        return False
    return not any(not n % i for i in range(3, int(math.sqrt(n) + 1), 2))


def _next_prime(value: int, factor: int = 1) -> int:
    value = factor * value
    orig = value
    while not _is_prime(value):
        value += 1
    if value == orig:
        return _next_prime(orig + 1)
    return value


# Variant 1: Linear Probing
class LinearProbingHashTable:
    """
    Hash table with linear probing collision resolution.
    Time: O(1) average insert/search, Space: O(n)

    >>> ht = LinearProbingHashTable(10)
    >>> ht.insert(10)
    >>> ht.insert(20)
    >>> ht.insert(30)
    >>> ht.search(20)
    True
    >>> ht.search(99)
    False
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.table = [None] * size

    def _hash(self, key: int) -> int:
        return key % self.size

    def insert(self, key: int) -> None:
        idx = self._hash(key)
        while self.table[idx] is not None and self.table[idx] != key:
            idx = (idx + 1) % self.size
        self.table[idx] = key

    def search(self, key: int) -> bool:
        idx = self._hash(key)
        start = idx
        while self.table[idx] is not None:
            if self.table[idx] == key:
                return True
            idx = (idx + 1) % self.size
            if idx == start:
                break
        return False


# Variant 2: Quadratic Probing
class QuadraticProbingHashTable:
    """
    Hash table with quadratic probing collision resolution.
    Time: O(1) average, better clustering than linear, Space: O(n)

    >>> ht = QuadraticProbingHashTable(11)
    >>> ht.insert(10)
    >>> ht.insert(21)
    >>> ht.insert(32)
    >>> ht.search(21)
    True
    >>> ht.search(99)
    False
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.table = [None] * size

    def _hash(self, key: int) -> int:
        return key % self.size

    def insert(self, key: int) -> None:
        idx = self._hash(key)
        i = 1
        while self.table[idx] is not None and self.table[idx] != key:
            idx = (self._hash(key) + i * i) % self.size
            i += 1
        self.table[idx] = key

    def search(self, key: int) -> bool:
        idx = self._hash(key)
        i = 1
        while self.table[idx] is not None:
            if self.table[idx] == key:
                return True
            idx = (self._hash(key) + i * i) % self.size
            i += 1
        return False


# Variant 3: Double Hashing
class DoubleHashingHashTable:
    """
    Hash table with double hashing collision resolution.
    Best distribution, no clustering, Time: O(1) average, Space: O(n)

    >>> ht = DoubleHashingHashTable(11)
    >>> ht.insert(10)
    >>> ht.insert(21)
    >>> ht.insert(32)
    >>> ht.search(21)
    True
    >>> ht.search(99)
    False
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.table = [None] * size
        self.prime = _next_prime(size - 1, factor=1) if size > 2 else 3

    def _hash1(self, key: int) -> int:
        return key % self.size

    def _hash2(self, key: int) -> int:
        return self.prime - (key % self.prime)

    def insert(self, key: int) -> None:
        idx = self._hash1(key)
        step = self._hash2(key)
        i = 0
        while self.table[idx] is not None and self.table[idx] != key:
            i += 1
            idx = (self._hash1(key) + i * step) % self.size
        self.table[idx] = key

    def search(self, key: int) -> bool:
        idx = self._hash1(key)
        step = self._hash2(key)
        i = 0
        while self.table[idx] is not None:
            if self.table[idx] == key:
                return True
            i += 1
            idx = (self._hash1(key) + i * step) % self.size
        return False


def benchmark():
    size = 997  # prime table size
    data = list(range(500))
    n = 1000

    def run_linear():
        ht = LinearProbingHashTable(size)
        for v in data:
            ht.insert(v)
        return all(ht.search(v) for v in data)

    def run_quadratic():
        ht = QuadraticProbingHashTable(size)
        for v in data:
            ht.insert(v)
        return all(ht.search(v) for v in data)

    def run_double():
        ht = DoubleHashingHashTable(size)
        for v in data:
            ht.insert(v)
        return all(ht.search(v) for v in data)

    t1 = timeit.timeit(run_linear, number=n)
    t2 = timeit.timeit(run_quadratic, number=n)
    t3 = timeit.timeit(run_double, number=n)

    print(f"linear_probing:     {t1:.4f}s for {n} runs")
    print(f"quadratic_probing:  {t2:.4f}s for {n} runs")
    print(f"double_hashing:     {t3:.4f}s for {n} runs")


if __name__ == "__main__":
    benchmark()
