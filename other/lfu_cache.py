"""
Least Frequently Used (LFU) Cache — Evicts the least frequently accessed item.

When capacity is exceeded, the item with the lowest access frequency is evicted.
Ties are broken by evicting the least recently used item among the least frequent.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/lfu_cache.py
"""

from __future__ import annotations

from collections import OrderedDict, defaultdict


class LFUCache:
    """
    LFU Cache with O(1) get and put.

    >>> cache = LFUCache(2)
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
        self.min_freq = 0
        self.key_to_val: dict[int, int] = {}
        self.key_to_freq: dict[int, int] = {}
        self.freq_to_keys: dict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)

    def _update_freq(self, key: int) -> None:
        """Increment frequency of key and maintain min_freq."""
        freq = self.key_to_freq[key]
        self.key_to_freq[key] = freq + 1
        del self.freq_to_keys[freq][key]

        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        self.freq_to_keys[freq + 1][key] = None

    def get(self, key: int) -> int:
        """Get value by key. Returns -1 if not found."""
        if key not in self.key_to_val:
            return -1
        self._update_freq(key)
        return self.key_to_val[key]

    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair."""
        if self.capacity <= 0:
            return

        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._update_freq(key)
            return

        if len(self.key_to_val) >= self.capacity:
            # Evict least frequently used (LRU among ties)
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]

        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
