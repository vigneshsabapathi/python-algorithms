"""
Circular Linked List — 3 Variants with Benchmark

Variant 1: Standard dataclass-based circular linked list
Variant 2: Sentinel-node approach (dummy head simplifies edge cases)
Variant 3: Array-backed circular buffer (O(1) all ops, fixed capacity)
"""

from __future__ import annotations

from dataclasses import dataclass
from timeit import timeit
from typing import Any


# ─── Variant 1: Standard Circular Linked List ──────────────────────────────

@dataclass
class NodeV1:
    data: Any
    next_node: NodeV1 | None = None


class CircularLinkedListV1:
    """Standard circular linked list with head/tail pointers."""

    def __init__(self):
        self.head = None
        self.tail = None

    def insert_tail(self, data):
        new_node = NodeV1(data)
        if self.head is None:
            new_node.next_node = new_node
            self.head = self.tail = new_node
        else:
            new_node.next_node = self.head
            self.tail.next_node = new_node
            self.tail = new_node

    def to_list(self):
        result = []
        if not self.head:
            return result
        node = self.head
        while True:
            result.append(node.data)
            node = node.next_node
            if node == self.head:
                break
        return result


# ─── Variant 2: Sentinel-Node approach ─────────────────────────────────────

@dataclass
class NodeV2:
    data: Any
    next_node: NodeV2 | None = None


class CircularLinkedListV2:
    """Circular linked list with a sentinel (dummy) node for cleaner logic."""

    def __init__(self):
        # Sentinel node — always present, never holds real data
        self._sentinel = NodeV2(None)
        self._sentinel.next_node = self._sentinel
        self._size = 0

    def insert_tail(self, data):
        new_node = NodeV2(data)
        # Find last real node (node before sentinel)
        temp = self._sentinel
        while temp.next_node != self._sentinel:
            temp = temp.next_node
        temp.next_node = new_node
        new_node.next_node = self._sentinel
        self._size += 1

    def to_list(self):
        result = []
        node = self._sentinel.next_node
        while node != self._sentinel:
            result.append(node.data)
            node = node.next_node
        return result

    def __len__(self):
        return self._size


# ─── Variant 3: Array-backed circular buffer ────────────────────────────────

class CircularBufferV3:
    """
    Fixed-capacity circular buffer (ring buffer) using an array.
    All operations O(1). More cache-friendly than pointer-based.
    """

    def __init__(self, capacity: int):
        self._buf = [None] * capacity
        self._capacity = capacity
        self._head = 0
        self._size = 0

    def enqueue(self, data):
        if self._size >= self._capacity:
            raise OverflowError("Buffer is full")
        tail = (self._head + self._size) % self._capacity
        self._buf[tail] = data
        self._size += 1

    def dequeue(self):
        if self._size == 0:
            raise IndexError("Buffer is empty")
        data = self._buf[self._head]
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return data

    def to_list(self):
        return [self._buf[(self._head + i) % self._capacity] for i in range(self._size)]

    def __len__(self):
        return self._size


# ─── Benchmark ─────────────────────────────────────────────────────────────

def benchmark():
    n = 500

    def build_v1():
        ll = CircularLinkedListV1()
        for i in range(n):
            ll.insert_tail(i)
        ll.to_list()

    def build_v2():
        ll = CircularLinkedListV2()
        for i in range(n):
            ll.insert_tail(i)
        ll.to_list()

    def build_v3():
        cb = CircularBufferV3(n)
        for i in range(n):
            cb.enqueue(i)
        cb.to_list()

    t1 = timeit(build_v1, number=200)
    t2 = timeit(build_v2, number=200)
    t3 = timeit(build_v3, number=200)

    print(f"Variant 1 (standard CLL):          {t1:.4f}s")
    print(f"Variant 2 (sentinel-node CLL):     {t2:.4f}s")
    print(f"Variant 3 (array ring buffer):     {t3:.4f}s")
    print(f"Speedup V3 vs V1: {t1/t3:.2f}x")


if __name__ == "__main__":
    # Verify correctness
    v1 = CircularLinkedListV1()
    for i in range(1, 6):
        v1.insert_tail(i)
    print("V1:", v1.to_list())

    v2 = CircularLinkedListV2()
    for i in range(1, 6):
        v2.insert_tail(i)
    print("V2:", v2.to_list())

    v3 = CircularBufferV3(10)
    for i in range(1, 6):
        v3.enqueue(i)
    print("V3:", v3.to_list())

    print()
    benchmark()
