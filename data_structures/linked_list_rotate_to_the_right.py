from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    data: int
    next_node: Node | None = None


def print_linked_list(head: Node | None) -> None:
    """
    Print the entire linked list iteratively.

    >>> head = insert_node(None, 0)
    >>> head = insert_node(head, 2)
    >>> head = insert_node(head, 1)
    >>> print_linked_list(head)
    0->2->1
    >>> head = insert_node(head, 4)
    >>> head = insert_node(head, 5)
    >>> print_linked_list(head)
    0->2->1->4->5
    """
    if head is None:
        return
    while head.next_node is not None:
        print(head.data, end="->")
        head = head.next_node
    print(head.data)


def insert_node(head: Node | None, data: int) -> Node:
    """
    Insert a new node at the end of a linked list and return the new head.

    >>> head = insert_node(None, 10)
    >>> head = insert_node(head, 9)
    >>> head = insert_node(head, 8)
    >>> print_linked_list(head)
    10->9->8
    """
    new_node = Node(data)
    if head is None:
        return new_node

    temp_node = head
    while temp_node.next_node:
        temp_node = temp_node.next_node

    temp_node.next_node = new_node
    return head


def rotate_to_the_right(head: Node, places: int) -> Node:
    """
    Rotate a linked list to the right by places times.

    >>> rotate_to_the_right(None, places=1)
    Traceback (most recent call last):
        ...
    ValueError: The linked list is empty.
    >>> head = insert_node(None, 1)
    >>> rotate_to_the_right(head, places=1) == head
    True
    >>> head = insert_node(None, 1)
    >>> head = insert_node(head, 2)
    >>> head = insert_node(head, 3)
    >>> head = insert_node(head, 4)
    >>> head = insert_node(head, 5)
    >>> new_head = rotate_to_the_right(head, places=2)
    >>> print_linked_list(new_head)
    4->5->1->2->3
    """
    if not head:
        raise ValueError("The linked list is empty.")

    if head.next_node is None:
        return head

    length = 1
    temp_node = head
    while temp_node.next_node is not None:
        length += 1
        temp_node = temp_node.next_node

    places %= length

    if places == 0:
        return head

    new_head_index = length - places

    temp_node = head
    for _ in range(new_head_index - 1):
        assert temp_node.next_node
        temp_node = temp_node.next_node

    assert temp_node.next_node
    new_head = temp_node.next_node
    temp_node.next_node = None
    temp_node = new_head
    while temp_node.next_node:
        temp_node = temp_node.next_node
    temp_node.next_node = head

    assert new_head
    return new_head


if __name__ == "__main__":
    import doctest

    doctest.testmod()
