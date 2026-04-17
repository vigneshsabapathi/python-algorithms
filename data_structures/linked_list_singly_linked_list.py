from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    """
    Create and initialize Node class instance.
    >>> Node(20)
    Node(20)
    >>> Node("Hello, world!")
    Node(Hello, world!)
    >>> Node(None)
    Node(None)
    >>> Node(True)
    Node(True)
    """

    data: Any
    next_node: Node | None = None

    def __repr__(self) -> str:
        """
        >>> Node(10).__repr__()
        'Node(10)'
        >>> repr(Node(10))
        'Node(10)'
        >>> Node(10)
        Node(10)
        """
        return f"Node({self.data})"


class LinkedList:
    def __init__(self):
        """
        >>> linked_list = LinkedList()
        >>> linked_list.head is None
        True
        """
        self.head = None

    def __iter__(self) -> Iterator[Any]:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("tail")
        >>> linked_list.insert_tail("tail_1")
        >>> linked_list.insert_tail("tail_2")
        >>> for node in linked_list:
        ...     node
        'tail'
        'tail_1'
        'tail_2'
        """
        node = self.head
        while node:
            yield node.data
            node = node.next_node

    def __len__(self) -> int:
        """
        >>> linked_list = LinkedList()
        >>> len(linked_list)
        0
        >>> linked_list.insert_tail("tail")
        >>> len(linked_list)
        1
        >>> linked_list.insert_head("head")
        >>> len(linked_list)
        2
        >>> _ = linked_list.delete_tail()
        >>> len(linked_list)
        1
        >>> _ = linked_list.delete_head()
        >>> len(linked_list)
        0
        """
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail(1)
        >>> linked_list.insert_tail(3)
        >>> repr(linked_list)
        '1 -> 3'
        >>> linked_list.insert_tail(5)
        >>> f"{linked_list}"
        '1 -> 3 -> 5'
        """
        return " -> ".join([str(item) for item in self])

    def __getitem__(self, index: int) -> Any:
        """
        >>> linked_list = LinkedList()
        >>> for i in range(0, 10):
        ...     linked_list.insert_nth(i, i)
        >>> all(str(linked_list[i]) == str(i) for i in range(0, 10))
        True
        >>> linked_list[-10]
        Traceback (most recent call last):
            ...
        ValueError: list index out of range.
        >>> linked_list[len(linked_list)]
        Traceback (most recent call last):
            ...
        ValueError: list index out of range.
        """
        if not 0 <= index < len(self):
            raise ValueError("list index out of range.")
        for i, node in enumerate(self):
            if i == index:
                return node
        return None

    def __setitem__(self, index: int, data: Any) -> None:
        """
        >>> linked_list = LinkedList()
        >>> for i in range(0, 10):
        ...     linked_list.insert_nth(i, i)
        >>> linked_list[0] = 666
        >>> linked_list[0]
        666
        >>> linked_list[5] = -666
        >>> linked_list[5]
        -666
        >>> linked_list[-10] = 666
        Traceback (most recent call last):
            ...
        ValueError: list index out of range.
        >>> linked_list[len(linked_list)] = 666
        Traceback (most recent call last):
            ...
        ValueError: list index out of range.
        """
        if not 0 <= index < len(self):
            raise ValueError("list index out of range.")
        current = self.head
        for _ in range(index):
            current = current.next_node
        current.data = data

    def insert_tail(self, data: Any) -> None:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("tail")
        >>> linked_list
        tail
        >>> linked_list.insert_tail("tail_2")
        >>> linked_list
        tail -> tail_2
        """
        self.insert_nth(len(self), data)

    def insert_head(self, data: Any) -> None:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.insert_head("head")
        >>> linked_list
        head
        >>> linked_list.insert_head("head_2")
        >>> linked_list
        head_2 -> head
        """
        self.insert_nth(0, data)

    def insert_nth(self, index: int, data: Any) -> None:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.insert_tail("third")
        >>> linked_list
        first -> second -> third
        >>> linked_list.insert_nth(1, "fourth")
        >>> linked_list
        first -> fourth -> second -> third
        """
        if not 0 <= index <= len(self):
            raise IndexError("list index out of range")
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        elif index == 0:
            new_node.next_node = self.head
            self.head = new_node
        else:
            temp = self.head
            for _ in range(index - 1):
                temp = temp.next_node
            new_node.next_node = temp.next_node
            temp.next_node = new_node

    def print_list(self) -> None:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list
        first -> second
        """
        print(self)

    def delete_head(self) -> Any:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.delete_head()
        'first'
        >>> linked_list.delete_head()
        'second'
        >>> linked_list.delete_head()
        Traceback (most recent call last):
            ...
        IndexError: List index out of range.
        """
        return self.delete_nth(0)

    def delete_tail(self) -> Any:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.delete_tail()
        'second'
        >>> linked_list.delete_tail()
        'first'
        >>> linked_list.delete_tail()
        Traceback (most recent call last):
            ...
        IndexError: List index out of range.
        """
        return self.delete_nth(len(self) - 1)

    def delete_nth(self, index: int = 0) -> Any:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.insert_tail("third")
        >>> linked_list.delete_nth(1)
        'second'
        >>> linked_list
        first -> third
        >>> linked_list.delete_nth(5)
        Traceback (most recent call last):
            ...
        IndexError: List index out of range.
        >>> linked_list.delete_nth(-1)
        Traceback (most recent call last):
            ...
        IndexError: List index out of range.
        """
        if not 0 <= index <= len(self) - 1:
            raise IndexError("List index out of range.")
        delete_node = self.head
        if index == 0:
            self.head = self.head.next_node
        else:
            temp = self.head
            for _ in range(index - 1):
                temp = temp.next_node
            delete_node = temp.next_node
            temp.next_node = temp.next_node.next_node
        return delete_node.data

    def is_empty(self) -> bool:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.is_empty()
        True
        >>> linked_list.insert_head("first")
        >>> linked_list.is_empty()
        False
        """
        return self.head is None

    def reverse(self) -> None:
        """
        >>> linked_list = LinkedList()
        >>> linked_list.insert_tail("first")
        >>> linked_list.insert_tail("second")
        >>> linked_list.insert_tail("third")
        >>> linked_list.reverse()
        >>> linked_list
        third -> second -> first
        """
        prev = None
        current = self.head

        while current:
            next_node = current.next_node
            current.next_node = prev
            prev = current
            current = next_node
        self.head = prev


def test_singly_linked_list() -> None:
    """
    >>> test_singly_linked_list()
    """
    linked_list = LinkedList()
    assert linked_list.is_empty() is True
    assert str(linked_list) == ""

    try:
        linked_list.delete_head()
        raise AssertionError
    except IndexError:
        assert True

    try:
        linked_list.delete_tail()
        raise AssertionError
    except IndexError:
        assert True

    for i in range(10):
        assert len(linked_list) == i
        linked_list.insert_nth(i, i + 1)
    assert str(linked_list) == " -> ".join(str(i) for i in range(1, 11))

    linked_list.insert_head(0)
    linked_list.insert_tail(11)
    assert str(linked_list) == " -> ".join(str(i) for i in range(12))

    assert linked_list.delete_head() == 0
    assert linked_list.delete_nth(9) == 10
    assert linked_list.delete_tail() == 11
    assert len(linked_list) == 9
    assert str(linked_list) == " -> ".join(str(i) for i in range(1, 10))

    assert all(linked_list[i] == i + 1 for i in range(9)) is True

    for i in range(9):
        linked_list[i] = -i
    assert all(linked_list[i] == -i for i in range(9)) is True

    linked_list.reverse()
    assert str(linked_list) == " -> ".join(str(i) for i in range(-8, 1))


if __name__ == "__main__":
    from doctest import testmod

    testmod()
