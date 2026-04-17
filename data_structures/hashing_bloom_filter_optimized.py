"""
Optimized variants of Bloom Filter.

Three implementations using different hash strategies and bitarray representations.
Benchmarks using timeit.
"""

import timeit
from hashlib import md5, sha256


# Variant 1: Original — bitwise integer as bit array
class BloomOriginal:
    """
    Original Bloom filter using bitwise integer and sha256+md5.

    >>> b = BloomOriginal(size=16)
    >>> b.add("hello")
    >>> "hello" in b
    True
    >>> "world" in b
    False
    """

    HASH_FUNCTIONS = (sha256, md5)

    def __init__(self, size: int = 8) -> None:
        self.bitarray = 0b0
        self.size = size

    def add(self, value: str) -> None:
        self.bitarray |= self.hash_(value)

    def exists(self, value: str) -> bool:
        h = self.hash_(value)
        return (h & self.bitarray) == h

    def __contains__(self, other: str) -> bool:
        return self.exists(other)

    def hash_(self, value: str) -> int:
        res = 0b0
        for func in self.HASH_FUNCTIONS:
            position = (
                int.from_bytes(func(value.encode()).digest(), "little") % self.size
            )
            res |= 2**position
        return res


# Variant 2: Bytearray-based bit array (more memory-efficient for large sizes)
class BloomBytearray:
    """
    Bloom filter using bytearray for the bit array (better for large sizes).

    >>> b = BloomBytearray(size=256)
    >>> b.add("hello")
    >>> "hello" in b
    True
    >>> "world" in b
    False
    """

    HASH_FUNCTIONS = (sha256, md5)

    def __init__(self, size: int = 256) -> None:
        self.size = size
        # size bits, stored in ceil(size/8) bytes
        self.bitarray = bytearray((size + 7) // 8)

    def _set_bit(self, pos: int) -> None:
        self.bitarray[pos // 8] |= 1 << (pos % 8)

    def _get_bit(self, pos: int) -> bool:
        return bool(self.bitarray[pos // 8] & (1 << (pos % 8)))

    def _positions(self, value: str) -> list[int]:
        return [
            int.from_bytes(func(value.encode()).digest(), "little") % self.size
            for func in self.HASH_FUNCTIONS
        ]

    def add(self, value: str) -> None:
        for pos in self._positions(value):
            self._set_bit(pos)

    def exists(self, value: str) -> bool:
        return all(self._get_bit(pos) for pos in self._positions(value))

    def __contains__(self, other: str) -> bool:
        return self.exists(other)


# Variant 3: Multiple hash functions via double hashing (Kirsch-Mitzenmacher)
class BloomDoubleHashing:
    """
    Bloom filter using Kirsch-Mitzenmacher double hashing trick.
    Simulates k hash functions using only 2 actual hashes.

    >>> b = BloomDoubleHashing(size=256, num_hashes=5)
    >>> b.add("hello")
    >>> "hello" in b
    True
    >>> "world" in b
    False
    """

    def __init__(self, size: int = 256, num_hashes: int = 5) -> None:
        self.size = size
        self.num_hashes = num_hashes
        self.bitarray = bytearray((size + 7) // 8)

    def _hashes(self, value: str) -> list[int]:
        h1 = int.from_bytes(sha256(value.encode()).digest(), "little") % self.size
        h2 = int.from_bytes(md5(value.encode()).digest(), "little") % self.size
        return [(h1 + i * h2) % self.size for i in range(self.num_hashes)]

    def _set_bit(self, pos: int) -> None:
        self.bitarray[pos // 8] |= 1 << (pos % 8)

    def _get_bit(self, pos: int) -> bool:
        return bool(self.bitarray[pos // 8] & (1 << (pos % 8)))

    def add(self, value: str) -> None:
        for pos in self._hashes(value):
            self._set_bit(pos)

    def exists(self, value: str) -> bool:
        return all(self._get_bit(pos) for pos in self._hashes(value))

    def __contains__(self, other: str) -> bool:
        return self.exists(other)


def benchmark():
    words = [f"word_{i}" for i in range(200)]
    n = 500

    def run_original():
        b = BloomOriginal(size=1024)
        for w in words:
            b.add(w)
        return all(w in b for w in words)

    def run_bytearray():
        b = BloomBytearray(size=1024)
        for w in words:
            b.add(w)
        return all(w in b for w in words)

    def run_double():
        b = BloomDoubleHashing(size=1024, num_hashes=5)
        for w in words:
            b.add(w)
        return all(w in b for w in words)

    t1 = timeit.timeit(run_original, number=n)
    t2 = timeit.timeit(run_bytearray, number=n)
    t3 = timeit.timeit(run_double, number=n)

    print(f"bitwise_int:     {t1:.4f}s for {n} runs")
    print(f"bytearray:       {t2:.4f}s for {n} runs")
    print(f"double_hashing:  {t3:.4f}s for {n} runs")


if __name__ == "__main__":
    benchmark()
