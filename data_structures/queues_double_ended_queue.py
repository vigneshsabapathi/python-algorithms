"""
Implementation of double ended queue (Deque).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


class Deque:
    """
    Deque data structure.
    Operations: append, appendleft, extend, extendleft, pop, popleft.

    >>> our_deque = Deque([1, 2, 3])
    >>> our_deque
    [1, 2, 3]
    >>> our_deque.append(4)
    >>> our_deque
    [1, 2, 3, 4]
    >>> our_deque.appendleft(0)
    >>> our_deque
    [0, 1, 2, 3, 4]
    >>> our_deque.pop()
    4
    >>> our_deque.popleft()
    0
    >>> our_deque
    [1, 2, 3]
    """

    __slots__ = ("_back", "_front", "_len")

    @dataclass
    class _Node:
        val: Any = None
        next_node: Deque._Node | None = None
        prev_node: Deque._Node | None = None

    class _Iterator:
        __slots__ = ("_cur",)

        def __init__(self, cur: Deque._Node | None) -> None:
            self._cur = cur

        def __iter__(self) -> Deque._Iterator:
            """
            >>> our_deque = Deque([1, 2, 3])
            >>> iterator = iter(our_deque)
            """
            return self

        def __next__(self) -> Any:
            """
            >>> our_deque = Deque([1, 2, 3])
            >>> iterator = iter(our_deque)
            >>> next(iterator)
            1
            >>> next(iterator)
            2
            >>> next(iterator)
            3
            """
            if self._cur is None:
                raise StopIteration
            val = self._cur.val
            self._cur = self._cur.next_node
            return val

    def __init__(self, iterable: Iterable[Any] | None = None) -> None:
        self._front: Any = None
        self._back: Any = None
        self._len: int = 0

        if iterable is not None:
            for val in iterable:
                self.append(val)

    def append(self, val: Any) -> None:
        """
        Adds val to the end of the deque. O(1).

        >>> our_deque_1 = Deque([1, 2, 3])
        >>> our_deque_1.append(4)
        >>> our_deque_1
        [1, 2, 3, 4]
        """
        node = self._Node(val, None, None)
        if self.is_empty():
            self._front = self._back = node
            self._len = 1
        else:
            self._back.next_node = node
            node.prev_node = self._back
            self._back = node
            self._len += 1
            assert not self.is_empty(), "Error on appending value."

    def appendleft(self, val: Any) -> None:
        """
        Adds val to the beginning of the deque. O(1).

        >>> our_deque_1 = Deque([2, 3])
        >>> our_deque_1.appendleft(1)
        >>> our_deque_1
        [1, 2, 3]
        """
        node = self._Node(val, None, None)
        if self.is_empty():
            self._front = self._back = node
            self._len = 1
        else:
            node.next_node = self._front
            self._front.prev_node = node
            self._front = node
            self._len += 1
            assert not self.is_empty(), "Error on appending value."

    def extend(self, iterable: Iterable[Any]) -> None:
        """
        Appends every value of iterable to the end. O(n).

        >>> our_deque_1 = Deque([1, 2, 3])
        >>> our_deque_1.extend([4, 5])
        >>> our_deque_1
        [1, 2, 3, 4, 5]
        """
        for val in iterable:
            self.append(val)

    def extendleft(self, iterable: Iterable[Any]) -> None:
        """
        Appends every value of iterable to the beginning. O(n).

        >>> our_deque_1 = Deque([1, 2, 3])
        >>> our_deque_1.extendleft([0, -1])
        >>> our_deque_1
        [-1, 0, 1, 2, 3]
        """
        for val in iterable:
            self.appendleft(val)

    def pop(self) -> Any:
        """
        Removes and returns the last element. O(1).

        >>> our_deque2 = Deque([1, 2, 3, 15182])
        >>> our_deque2.pop()
        15182
        >>> our_deque2
        [1, 2, 3]
        """
        assert not self.is_empty(), "Deque is empty."

        topop = self._back
        if self._front == self._back:
            self._front = None
            self._back = None
        else:
            self._back = self._back.prev_node
            self._back.next_node = None

        self._len -= 1
        return topop.val

    def popleft(self) -> Any:
        """
        Removes and returns the first element. O(1).

        >>> our_deque2 = Deque([15182, 1, 2, 3])
        >>> our_deque2.popleft()
        15182
        >>> our_deque2
        [1, 2, 3]
        """
        assert not self.is_empty(), "Deque is empty."

        topop = self._front
        if self._front == self._back:
            self._front = None
            self._back = None
        else:
            self._front = self._front.next_node
            self._front.prev_node = None

        self._len -= 1
        return topop.val

    def is_empty(self) -> bool:
        """
        >>> our_deque = Deque([1, 2, 3])
        >>> our_deque.is_empty()
        False
        >>> our_empty_deque = Deque()
        >>> our_empty_deque.is_empty()
        True
        """
        return self._front is None

    def __len__(self) -> int:
        """
        >>> our_deque = Deque([1, 2, 3])
        >>> len(our_deque)
        3
        >>> our_empty_deque = Deque()
        >>> len(our_empty_deque)
        0
        """
        return self._len

    def __eq__(self, other: object) -> bool:
        """
        >>> our_deque_1 = Deque([1, 2, 3])
        >>> our_deque_2 = Deque([1, 2, 3])
        >>> our_deque_1 == our_deque_2
        True
        >>> our_deque_3 = Deque([1, 2])
        >>> our_deque_1 == our_deque_3
        False
        """
        if not isinstance(other, Deque):
            return NotImplemented

        me = self._front
        oth = other._front

        if len(self) != len(other):
            return False

        while me is not None and oth is not None:
            if me.val != oth.val:
                return False
            me = me.next_node
            oth = oth.next_node

        return True

    def __iter__(self) -> Deque._Iterator:
        """
        >>> our_deque = Deque([1, 2, 3])
        >>> for v in our_deque:
        ...     print(v)
        1
        2
        3
        """
        return Deque._Iterator(self._front)

    def __repr__(self) -> str:
        """
        >>> our_deque = Deque([1, 2, 3])
        >>> our_deque
        [1, 2, 3]
        """
        values_list = []
        aux = self._front
        while aux is not None:
            values_list.append(aux.val)
            aux = aux.next_node

        return f"[{', '.join(repr(val) for val in values_list)}]"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
