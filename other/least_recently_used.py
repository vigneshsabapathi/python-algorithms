"""
Least Recently Used (LRU) Cache — Manual implementation using doubly linked list + hashmap.

The LRU cache evicts the least recently accessed item when capacity is reached.
This implementation uses a doubly linked list for O(1) move-to-front and a
dictionary for O(1) lookup.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/least_recently_used.py
"""

from __future__ import annotations


class _Node:
    """Doubly linked list node."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key = key
        self.value = value
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCache:
    """
    LRU Cache with O(1) get and put operations.

    >>> cache = LRUCache(2)
    >>> cache.put(1, 1)
    >>> cache.put(2, 2)
    >>> cache.get(1)
    1
    >>> cache.put(3, 3)
    >>> cache.get(2)
    -1
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
        self.cache: dict[int, _Node] = {}
        # Sentinel nodes
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        """Remove node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node

    def _add_to_front(self, node: _Node) -> None:
        """Add node right after head (most recently used)."""
        node.prev = self.head
        node.next = self.head.next
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        """Get value by key, return -1 if not found."""
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        """Insert or update key-value pair."""
        if key in self.cache:
            self._remove(self.cache[key])
            del self.cache[key]

        node = _Node(key, value)
        self._add_to_front(node)
        self.cache[key] = node

        if len(self.cache) > self.capacity:
            # Evict least recently used (node before tail)
            lru = self.tail.prev
            if lru and lru != self.head:
                self._remove(lru)
                del self.cache[lru.key]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
