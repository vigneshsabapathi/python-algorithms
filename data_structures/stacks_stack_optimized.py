"""
Stack — 3 Variants with Benchmark

Variant 1: List-based stack (standard append/pop)
Variant 2: Linked list-based stack (node pointers)
Variant 3: collections.deque-based stack (thread-safe, O(1) both ends)
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from timeit import timeit
from typing import Any


# ─── Variant 1: List-backed Stack ──────────────────────────────────────────

class StackV1:
    """Standard list-backed stack. O(1) amortized push/pop."""

    def __init__(self):
        self._data: list[Any] = []

    def push(self, item: Any) -> None:
        self._data.append(item)

    def pop(self) -> Any:
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        if not self._data:
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return not self._data

    def size(self) -> int:
        return len(self._data)


# ─── Variant 2: Linked list-backed Stack ────────────────────────────────────

@dataclass
class _Node:
    data: Any
    next_node: _Node | None = None


class StackV2:
    """Linked list-backed stack. O(1) push/pop with no reallocation."""

    def __init__(self):
        self._top: _Node | None = None
        self._size = 0

    def push(self, item: Any) -> None:
        self._top = _Node(item, self._top)
        self._size += 1

    def pop(self) -> Any:
        if not self._top:
            raise IndexError("pop from empty stack")
        data = self._top.data
        self._top = self._top.next_node
        self._size -= 1
        return data

    def peek(self) -> Any:
        if not self._top:
            raise IndexError("peek from empty stack")
        return self._top.data

    def is_empty(self) -> bool:
        return self._top is None

    def size(self) -> int:
        return self._size


# ─── Variant 3: Deque-backed Stack ──────────────────────────────────────────

class StackV3:
    """
    Deque-backed stack. Python's deque is implemented in C,
    so it has faster O(1) append/pop than list in many scenarios.
    Also thread-safe for individual operations.
    """

    def __init__(self):
        self._data: deque = deque()

    def push(self, item: Any) -> None:
        self._data.append(item)

    def pop(self) -> Any:
        if not self._data:
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        if not self._data:
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return not self._data

    def size(self) -> int:
        return len(self._data)


# ─── Benchmark ─────────────────────────────────────────────────────────────

def benchmark():
    n = 10_000

    def run_v1():
        s = StackV1()
        for i in range(n):
            s.push(i)
        while not s.is_empty():
            s.pop()

    def run_v2():
        s = StackV2()
        for i in range(n):
            s.push(i)
        while not s.is_empty():
            s.pop()

    def run_v3():
        s = StackV3()
        for i in range(n):
            s.push(i)
        while not s.is_empty():
            s.pop()

    t1 = timeit(run_v1, number=100)
    t2 = timeit(run_v2, number=100)
    t3 = timeit(run_v3, number=100)

    print(f"Variant 1 (list-backed):       {t1:.4f}s")
    print(f"Variant 2 (linked list):       {t2:.4f}s")
    print(f"Variant 3 (deque-backed):      {t3:.4f}s")
    print(f"Speedup V3 vs V2: {t2/t3:.2f}x")


if __name__ == "__main__":
    # Verify correctness
    for cls in (StackV1, StackV2, StackV3):
        s = cls()
        for i in range(1, 6):
            s.push(i)
        print(f"{cls.__name__}: size={s.size()}, peek={s.peek()}, pop={s.pop()}")

    print()
    benchmark()
