from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    data: Any
    next_node: Node | None = None


@dataclass
class LinkedList:
    head: Node | None = None

    def __iter__(self) -> Iterator:
        """
        >>> linked_list = LinkedList()
        >>> list(linked_list)
        []
        >>> linked_list.push(0)
        >>> tuple(linked_list)
        (0,)
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
        >>> linked_list.push(0)
        >>> len(linked_list)
        1
        """
        return sum(1 for _ in self)

    def push(self, new_data: Any) -> None:
        """
        Add a new node with the given data to the beginning of the Linked List.

        >>> linked_list = LinkedList()
        >>> linked_list.push(5)
        >>> linked_list.push(4)
        >>> linked_list.push(3)
        >>> list(linked_list)
        [3, 4, 5]
        """
        new_node = Node(new_data)
        new_node.next_node = self.head
        self.head = new_node

    def swap_nodes(self, node_data_1: Any, node_data_2: Any) -> None:
        """
        Swap the positions of two nodes in the Linked List based on their data values.

        >>> linked_list = LinkedList()
        >>> for i in range(1, 6):
        ...     linked_list.push(6 - i)
        >>> list(linked_list)
        [1, 2, 3, 4, 5]
        >>> linked_list.swap_nodes(1, 5)
        >>> tuple(linked_list)
        (5, 2, 3, 4, 1)

        >>> second_list = LinkedList()
        >>> second_list.push(6)
        >>> second_list.swap_nodes(1, 6) is None
        True

        >>> empty_list = LinkedList()
        >>> empty_list.swap_nodes(1, 3) is None
        True
        """
        if node_data_1 == node_data_2:
            return

        node_1 = self.head
        while node_1 and node_1.data != node_data_1:
            node_1 = node_1.next_node

        node_2 = self.head
        while node_2 and node_2.data != node_data_2:
            node_2 = node_2.next_node

        if node_1 is None or node_2 is None:
            return

        node_1.data, node_2.data = node_2.data, node_1.data


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    linked_list = LinkedList()
    for i in range(5, 0, -1):
        linked_list.push(i)

    print(f"Original Linked List: {list(linked_list)}")
    linked_list.swap_nodes(1, 4)
    print(f"Modified Linked List: {list(linked_list)}")
    print("After swapping the nodes whose data is 1 and 4.")
