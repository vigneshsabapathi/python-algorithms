"""
Queue — 3 Variants with Benchmark

Variant 1: list.pop(0) — O(n) dequeue (naive)
Variant 2: Two-stack queue — O(1) amortized dequeue
Variant 3: collections.deque — O(1) enqueue and dequeue (best practice)
"""

from __future__ import annotations

from collections import deque
from timeit import timeit
from typing import Any


# ─── Variant 1: List-pop(0) queue (O(n) dequeue) ───────────────────────────

class QueueV1:
    """List-based queue using pop(0). Dequeue is O(n) — not recommended."""

    def __init__(self):
        self._data: list[Any] = []

    def enqueue(self, item: Any) -> None:
        self._data.append(item)

    def dequeue(self) -> Any:
        if not self._data:
            raise IndexError("dequeue from empty queue")
        return self._data.pop(0)  # O(n) — shifts all elements

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data


# ─── Variant 2: Two-stack queue (O(1) amortized) ────────────────────────────

class QueueV2:
    """
    Two-stack queue. Enqueue pushes to stack1; dequeue pops from stack2.
    When stack2 is empty, reverse stack1 into stack2. O(1) amortized.
    """

    def __init__(self):
        self._in: list[Any] = []
        self._out: list[Any] = []

    def enqueue(self, item: Any) -> None:
        self._in.append(item)

    def dequeue(self) -> Any:
        if not self._out:
            while self._in:
                self._out.append(self._in.pop())
        if not self._out:
            raise IndexError("dequeue from empty queue")
        return self._out.pop()

    def __len__(self) -> int:
        return len(self._in) + len(self._out)

    def is_empty(self) -> bool:
        return not self._in and not self._out


# ─── Variant 3: collections.deque queue (O(1) guaranteed) ──────────────────

class QueueV3:
    """
    Deque-backed queue. Python's collections.deque is O(1) for both
    appendleft and pop (implemented in C). Best practical choice.
    """

    def __init__(self):
        self._data: deque[Any] = deque()

    def enqueue(self, item: Any) -> None:
        self._data.append(item)

    def dequeue(self) -> Any:
        if not self._data:
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return not self._data


# ─── Benchmark ─────────────────────────────────────────────────────────────

def benchmark():
    n = 2_000

    def run_v1():
        q = QueueV1()
        for i in range(n):
            q.enqueue(i)
        while not q.is_empty():
            q.dequeue()

    def run_v2():
        q = QueueV2()
        for i in range(n):
            q.enqueue(i)
        while not q.is_empty():
            q.dequeue()

    def run_v3():
        q = QueueV3()
        for i in range(n):
            q.enqueue(i)
        while not q.is_empty():
            q.dequeue()

    t1 = timeit(run_v1, number=100)
    t2 = timeit(run_v2, number=100)
    t3 = timeit(run_v3, number=100)

    print(f"Variant 1 (list.pop(0), O(n)):    {t1:.4f}s")
    print(f"Variant 2 (two-stack, O(1) amort): {t2:.4f}s")
    print(f"Variant 3 (deque, O(1)):           {t3:.4f}s")
    print(f"Speedup V3 vs V1: {t1/t3:.2f}x")
    print(f"Speedup V2 vs V1: {t1/t2:.2f}x")


if __name__ == "__main__":
    for cls in (QueueV1, QueueV2, QueueV3):
        q = cls()
        for i in range(1, 6):
            q.enqueue(i)
        results = []
        while not q.is_empty():
            results.append(q.dequeue())
        print(f"{cls.__name__}: {results}")

    print()
    benchmark()
