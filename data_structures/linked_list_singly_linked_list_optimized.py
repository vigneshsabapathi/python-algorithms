"""
Singly Linked List — 3 Variants with Benchmark

Variant 1: Standard (standard pointer traversal, O(n) insert_tail)
Variant 2: Tail-optimized (tracks tail pointer, O(1) insert_tail)
Variant 3: Deque-backed (uses Python's collections.deque for O(1) both ends)
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from timeit import timeit
from typing import Any


# ─── Variant 1: Standard singly linked list ────────────────────────────────

@dataclass
class NodeV1:
    data: Any
    next_node: NodeV1 | None = None


class SinglyLinkedListV1:
    """Standard singly linked list — O(n) insert at tail."""

    def __init__(self):
        self.head = None

    def insert_tail(self, data):
        new_node = NodeV1(data)
        if not self.head:
            self.head = new_node
            return
        temp = self.head
        while temp.next_node:
            temp = temp.next_node
        temp.next_node = new_node

    def to_list(self):
        result = []
        node = self.head
        while node:
            result.append(node.data)
            node = node.next_node
        return result

    def reverse(self):
        prev, curr = None, self.head
        while curr:
            nxt = curr.next_node
            curr.next_node = prev
            prev = curr
            curr = nxt
        self.head = prev


# ─── Variant 2: Tail-pointer optimized ─────────────────────────────────────

@dataclass
class NodeV2:
    data: Any
    next_node: NodeV2 | None = None


class SinglyLinkedListV2:
    """Tail-pointer optimized singly linked list — O(1) insert at tail."""

    def __init__(self):
        self.head = None
        self.tail = None

    def insert_tail(self, data):
        new_node = NodeV2(data)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next_node = new_node
            self.tail = new_node

    def to_list(self):
        result = []
        node = self.head
        while node:
            result.append(node.data)
            node = node.next_node
        return result

    def reverse(self):
        prev, curr = None, self.head
        self.tail = self.head
        while curr:
            nxt = curr.next_node
            curr.next_node = prev
            prev = curr
            curr = nxt
        self.head = prev


# ─── Variant 3: Deque-backed (Python built-in) ─────────────────────────────

class SinglyLinkedListV3:
    """
    Deque-backed linked list — O(1) insert/remove at both ends.
    Uses Python's built-in deque for maximum speed.
    """

    def __init__(self):
        self._data = deque()

    def insert_tail(self, data):
        self._data.append(data)

    def insert_head(self, data):
        self._data.appendleft(data)

    def to_list(self):
        return list(self._data)

    def reverse(self):
        self._data = deque(reversed(self._data))


# ─── Benchmark ─────────────────────────────────────────────────────────────

def benchmark():
    n = 1000

    def build_v1():
        ll = SinglyLinkedListV1()
        for i in range(n):
            ll.insert_tail(i)
        ll.reverse()

    def build_v2():
        ll = SinglyLinkedListV2()
        for i in range(n):
            ll.insert_tail(i)
        ll.reverse()

    def build_v3():
        ll = SinglyLinkedListV3()
        for i in range(n):
            ll.insert_tail(i)
        ll.reverse()

    t1 = timeit(build_v1, number=200)
    t2 = timeit(build_v2, number=200)
    t3 = timeit(build_v3, number=200)

    print(f"Variant 1 (standard, O(n) tail):        {t1:.4f}s")
    print(f"Variant 2 (tail-pointer, O(1) tail):    {t2:.4f}s")
    print(f"Variant 3 (deque-backed):                {t3:.4f}s")
    print(f"Speedup V2 vs V1: {t1/t2:.2f}x")
    print(f"Speedup V3 vs V1: {t1/t3:.2f}x")


if __name__ == "__main__":
    # Verify correctness
    for cls in (SinglyLinkedListV1, SinglyLinkedListV2, SinglyLinkedListV3):
        ll = cls()
        for i in range(1, 6):
            ll.insert_tail(i)
        print(f"{cls.__name__}: {ll.to_list()}")

    print()
    benchmark()
