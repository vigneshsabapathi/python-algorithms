from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    data: Any
    next_node: Node | None = None


@dataclass
class CircularLinkedList:
    head: Node | None = None  # Reference to the head (first node)
    tail: Node | None = None  # Reference to the tail (last node)

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate through all nodes in the Circular Linked List yielding their data.

        >>> cll = CircularLinkedList()
        >>> cll.insert_tail(1)
        >>> cll.insert_tail(2)
        >>> cll.insert_tail(3)
        >>> list(cll)
        [1, 2, 3]
        """
        node = self.head
        while node:
            yield node.data
            node = node.next_node
            if node == self.head:
                break

    def __len__(self) -> int:
        """
        Get the length (number of nodes) in the Circular Linked List.

        >>> cll = CircularLinkedList()
        >>> len(cll)
        0
        >>> cll.insert_tail(1)
        >>> len(cll)
        1
        """
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        """
        Generate a string representation of the Circular Linked List.

        >>> cll = CircularLinkedList()
        >>> cll.insert_tail(1)
        >>> cll.insert_tail(2)
        >>> str(cll)
        '1->2'
        """
        return "->".join(str(item) for item in iter(self))

    def insert_tail(self, data: Any) -> None:
        """
        Insert a node with the given data at the end of the Circular Linked List.

        >>> cll = CircularLinkedList()
        >>> cll.insert_tail(10)
        >>> list(cll)
        [10]
        """
        self.insert_nth(len(self), data)

    def insert_head(self, data: Any) -> None:
        """
        Insert a node with the given data at the beginning of the Circular Linked List.

        >>> cll = CircularLinkedList()
        >>> cll.insert_head(10)
        >>> list(cll)
        [10]
        """
        self.insert_nth(0, data)

    def insert_nth(self, index: int, data: Any) -> None:
        """
        Insert the data of the node at the nth pos in the Circular Linked List.

        >>> cll = CircularLinkedList()
        >>> cll.insert_nth(0, 1)
        >>> cll.insert_nth(1, 2)
        >>> cll.insert_nth(2, 3)
        >>> list(cll)
        [1, 2, 3]
        >>> cll.insert_nth(-1, 99)
        Traceback (most recent call last):
            ...
        IndexError: list index out of range.
        """
        if index < 0 or index > len(self):
            raise IndexError("list index out of range.")
        new_node: Node = Node(data)
        if self.head is None:
            new_node.next_node = new_node  # First node points to itself
            self.tail = self.head = new_node
        elif index == 0:  # Insert at the head
            new_node.next_node = self.head
            assert self.tail is not None
            self.head = self.tail.next_node = new_node
        else:
            temp: Node | None = self.head
            for _ in range(index - 1):
                assert temp is not None
                temp = temp.next_node
            assert temp is not None
            new_node.next_node = temp.next_node
            temp.next_node = new_node
            if index == len(self) - 1:  # Insert at the tail
                self.tail = new_node

    def delete_front(self) -> Any:
        """
        Delete and return the data of the node at the front.

        >>> cll = CircularLinkedList()
        >>> cll.insert_tail(1)
        >>> cll.insert_tail(2)
        >>> cll.delete_front()
        1
        """
        return self.delete_nth(0)

    def delete_tail(self) -> Any:
        """
        Delete and return the data of the node at the end.

        >>> cll = CircularLinkedList()
        >>> cll.insert_tail(1)
        >>> cll.insert_tail(2)
        >>> cll.delete_tail()
        2
        """
        return self.delete_nth(len(self) - 1)

    def delete_nth(self, index: int = 0) -> Any:
        """
        Delete and return the data of the node at the nth position.

        >>> cll = CircularLinkedList()
        >>> cll.delete_nth(0)
        Traceback (most recent call last):
            ...
        IndexError: list index out of range.
        >>> for i in range(1, 4):
        ...     cll.insert_tail(i)
        >>> cll.delete_nth(1)
        2
        >>> list(cll)
        [1, 3]
        """
        if not 0 <= index < len(self):
            raise IndexError("list index out of range.")

        assert self.head is not None
        assert self.tail is not None
        delete_node: Node = self.head
        if self.head == self.tail:  # Just one node
            self.head = self.tail = None
        elif index == 0:  # Delete head node
            assert self.tail.next_node is not None
            self.tail.next_node = self.tail.next_node.next_node
            self.head = self.head.next_node
        else:
            temp: Node | None = self.head
            for _ in range(index - 1):
                assert temp is not None
                temp = temp.next_node
            assert temp is not None
            assert temp.next_node is not None
            delete_node = temp.next_node
            temp.next_node = temp.next_node.next_node
            if index == len(self) - 1:  # Delete at tail
                self.tail = temp
        return delete_node.data

    def is_empty(self) -> bool:
        """
        Check if the Circular Linked List is empty.

        >>> CircularLinkedList().is_empty()
        True
        """
        return len(self) == 0


def test_circular_linked_list() -> None:
    """
    >>> test_circular_linked_list()
    """
    cll = CircularLinkedList()
    assert len(cll) == 0
    assert cll.is_empty() is True
    assert str(cll) == ""

    try:
        cll.delete_front()
        raise AssertionError
    except IndexError:
        assert True

    try:
        cll.delete_tail()
        raise AssertionError
    except IndexError:
        assert True

    for i in range(5):
        assert len(cll) == i
        cll.insert_nth(i, i + 1)
    assert str(cll) == "->".join(str(i) for i in range(1, 6))

    cll.insert_tail(6)
    assert str(cll) == "->".join(str(i) for i in range(1, 7))
    cll.insert_head(0)
    assert str(cll) == "->".join(str(i) for i in range(7))

    assert cll.delete_front() == 0
    assert cll.delete_tail() == 6
    assert str(cll) == "->".join(str(i) for i in range(1, 6))
    assert cll.delete_nth(2) == 3

    cll.insert_nth(2, 3)
    assert str(cll) == "->".join(str(i) for i in range(1, 6))
    assert cll.is_empty() is False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
