from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ListNode:
    val: int = 0
    next_node: ListNode | None = None


def is_palindrome(head: ListNode | None) -> bool:
    """
    Check if a linked list is a palindrome.

    >>> is_palindrome(None)
    True
    >>> is_palindrome(ListNode(1))
    True
    >>> is_palindrome(ListNode(1, ListNode(2)))
    False
    >>> is_palindrome(ListNode(1, ListNode(2, ListNode(1))))
    True
    >>> is_palindrome(ListNode(1, ListNode(2, ListNode(2, ListNode(1)))))
    True
    """
    if not head:
        return True
    fast: ListNode | None = head.next_node
    slow: ListNode | None = head
    while fast and fast.next_node:
        fast = fast.next_node.next_node
        slow = slow.next_node if slow else None
    if slow:
        second = slow.next_node
        slow.next_node = None
    node: ListNode | None = None
    while second:
        nxt = second.next_node
        second.next_node = node
        node = second
        second = nxt
    while node and head:
        if node.val != head.val:
            return False
        node = node.next_node
        head = head.next_node
    return True


def is_palindrome_stack(head: ListNode | None) -> bool:
    """
    Check if a linked list is a palindrome using a stack.

    >>> is_palindrome_stack(None)
    True
    >>> is_palindrome_stack(ListNode(1))
    True
    >>> is_palindrome_stack(ListNode(1, ListNode(2)))
    False
    >>> is_palindrome_stack(ListNode(1, ListNode(2, ListNode(1))))
    True
    >>> is_palindrome_stack(ListNode(1, ListNode(2, ListNode(2, ListNode(1)))))
    True
    """
    if not head or not head.next_node:
        return True

    slow: ListNode | None = head
    fast: ListNode | None = head
    while fast and fast.next_node:
        fast = fast.next_node.next_node
        slow = slow.next_node if slow else None

    if slow:
        stack = [slow.val]
        while slow.next_node:
            slow = slow.next_node
            stack.append(slow.val)

        cur: ListNode | None = head
        while stack and cur:
            if stack.pop() != cur.val:
                return False
            cur = cur.next_node

    return True


def is_palindrome_dict(head: ListNode | None) -> bool:
    """
    Check if a linked list is a palindrome using a dictionary.

    >>> is_palindrome_dict(None)
    True
    >>> is_palindrome_dict(ListNode(1))
    True
    >>> is_palindrome_dict(ListNode(1, ListNode(2)))
    False
    >>> is_palindrome_dict(ListNode(1, ListNode(2, ListNode(1))))
    True
    >>> is_palindrome_dict(ListNode(1, ListNode(2, ListNode(2, ListNode(1)))))
    True
    >>> is_palindrome_dict(
    ...     ListNode(
    ...         1, ListNode(2, ListNode(1, ListNode(3, ListNode(2, ListNode(1)))))
    ...     )
    ... )
    False
    """
    if not head or not head.next_node:
        return True
    d: dict[int, list[int]] = {}
    pos = 0
    while head:
        if head.val in d:
            d[head.val].append(pos)
        else:
            d[head.val] = [pos]
        head = head.next_node
        pos += 1
    checksum = pos - 1
    middle = 0
    for v in d.values():
        if len(v) % 2 != 0:
            middle += 1
        else:
            for step, i in enumerate(range(len(v))):
                if v[i] + v[len(v) - 1 - step] != checksum:
                    return False
        if middle > 1:
            return False
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
