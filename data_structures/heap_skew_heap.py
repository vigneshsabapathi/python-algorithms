#!/usr/bin/env python3
"""
Skew Heap — a self-adjusting heap data structure.
Supports insertion and min extraction in amortized O(log N) time.

Wiki: https://en.wikipedia.org/wiki/Skew_heap
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, TypeVar

T = TypeVar("T", bound=bool)


class SkewNode[T: bool]:
    """
    One node of the skew heap. Contains the value and references to
    two children.
    """

    def __init__(self, value: T) -> None:
        self._value: T = value
        self.left: SkewNode[T] | None = None
        self.right: SkewNode[T] | None = None

    @property
    def value(self) -> T:
        """Return the value of the node."""
        return self._value

    @staticmethod
    def merge(
        root1: SkewNode[T] | None, root2: SkewNode[T] | None
    ) -> SkewNode[T] | None:
        """Merge 2 nodes together."""
        if not root1:
            return root2
        if not root2:
            return root1
        if root1.value > root2.value:
            root1, root2 = root2, root1
        result = root1
        temp = root1.right
        result.right = root1.left
        result.left = SkewNode.merge(temp, root2)
        return result


class SkewHeap[T: bool]:
    """
    A data structure allowing insertion and removal of smallest values
    in amortized O(log N) time.

    >>> sh = SkewHeap([3, 1, 4, 1, 5, 9])
    >>> sh.top()
    1
    >>> sh.pop()
    1
    >>> sh.pop()
    1
    >>> sh.pop()
    3

    >>> rh = SkewHeap()
    >>> rh.pop()
    Traceback (most recent call last):
        ...
    IndexError: Can't get top element for the empty heap.

    >>> rh.insert(5)
    >>> rh.insert(2)
    >>> rh.insert(8)
    >>> rh.top()
    2
    """

    def __init__(self, data: Iterable[T] | None = ()) -> None:
        self._root: SkewNode[T] | None = None
        if data:
            for item in data:
                self.insert(item)

    def __bool__(self) -> bool:
        return self._root is not None

    def __iter__(self) -> Iterator[T]:
        result: list[Any] = []
        while self:
            result.append(self.pop())
        for item in result:
            self.insert(item)
        return iter(result)

    def insert(self, value: T) -> None:
        """
        Insert a value into the heap.

        >>> sh = SkewHeap()
        >>> sh.insert(10)
        >>> sh.insert(5)
        >>> sh.top()
        5
        """
        self._root = SkewNode.merge(self._root, SkewNode(value))

    def pop(self) -> T | None:
        """
        Pop and return the minimum value.

        >>> sh = SkewHeap([4, 2, 6])
        >>> sh.pop()
        2
        >>> sh.pop()
        4
        """
        result = self.top()
        self._root = (
            SkewNode.merge(self._root.left, self._root.right) if self._root else None
        )
        return result

    def top(self) -> T:
        """
        Return the minimum value without removing.

        >>> sh = SkewHeap([7, 3, 5])
        >>> sh.top()
        3
        """
        if not self._root:
            raise IndexError("Can't get top element for the empty heap.")
        return self._root.value

    def clear(self) -> None:
        """
        Clear the heap.

        >>> sh = SkewHeap([1, 2, 3])
        >>> sh.clear()
        >>> bool(sh)
        False
        """
        self._root = None


if __name__ == "__main__":
    import doctest

    doctest.testmod()
