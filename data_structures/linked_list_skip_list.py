"""
Based on "Skip Lists: A Probabilistic Alternative to Balanced Trees" by William Pugh
https://epaperpress.com/sortsearch/download/skiplist.pdf
"""

from __future__ import annotations

from itertools import pairwise
from random import random
from typing import TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


class Node:
    def __init__(self, key="root", value=None):
        self.key = key
        self.value = value
        self.forward: list[Node] = []

    def __repr__(self) -> str:
        """
        >>> node = Node("Key", 2)
        >>> repr(node)
        'Node(Key: 2)'
        """
        return f"Node({self.key}: {self.value})"

    @property
    def level(self) -> int:
        """
        >>> node = Node("Key", 2)
        >>> node.level
        0
        >>> node.forward.append(Node("Key2", 4))
        >>> node.level
        1
        >>> node.forward.append(Node("Key3", 6))
        >>> node.level
        2
        """
        return len(self.forward)


class SkipList:
    def __init__(self, p: float = 0.5, max_level: int = 16):
        self.head: Node = Node()
        self.level = 0
        self.p = p
        self.max_level = max_level

    def __str__(self) -> str:
        """
        >>> skip_list = SkipList()
        >>> print(skip_list)
        SkipList(level=0)
        >>> skip_list.insert("Key1", "Value")
        >>> print(skip_list) # doctest: +ELLIPSIS
        SkipList(level=...
        [root]--...
        [Key1]--Key1...
        None    *...
        >>> skip_list.insert("Key2", "OtherValue")
        >>> print(skip_list) # doctest: +ELLIPSIS
        SkipList(level=...
        [root]--...
        [Key1]--Key1...
        [Key2]--Key2...
        None    *...
        """
        items = list(self)

        if len(items) == 0:
            return f"SkipList(level={self.level})"

        label_size = max((len(str(item)) for item in items), default=4)
        label_size = max(label_size, 4) + 4

        node = self.head
        lines = []

        forwards = node.forward.copy()
        lines.append(f"[{node.key}]".ljust(label_size, "-") + "* " * len(forwards))
        lines.append(" " * label_size + "| " * len(forwards))

        while len(node.forward) != 0:
            node = node.forward[0]

            lines.append(
                f"[{node.key}]".ljust(label_size, "-")
                + " ".join(str(n.key) if n.key == node.key else "|" for n in forwards)
            )
            lines.append(" " * label_size + "| " * len(forwards))
            forwards[: node.level] = node.forward

        lines.append("None".ljust(label_size) + "* " * len(forwards))
        return f"SkipList(level={self.level})\n" + "\n".join(lines)

    def __iter__(self):
        node = self.head
        while len(node.forward) != 0:
            yield node.forward[0].key
            node = node.forward[0]

    def random_level(self) -> int:
        level = 1
        while random() < self.p and level < self.max_level:
            level += 1
        return level

    def _locate_node(self, key) -> tuple[Node | None, list[Node]]:
        update_vector = []
        node = self.head

        for i in reversed(range(self.level)):
            while i < node.level and node.forward[i].key < key:
                node = node.forward[i]
            update_vector.append(node)

        update_vector.reverse()

        if len(node.forward) != 0 and node.forward[0].key == key:
            return node.forward[0], update_vector
        else:
            return None, update_vector

    def delete(self, key):
        """
        >>> skip_list = SkipList()
        >>> skip_list.insert(2, "Two")
        >>> skip_list.insert(1, "One")
        >>> skip_list.insert(3, "Three")
        >>> list(skip_list)
        [1, 2, 3]
        >>> skip_list.delete(2)
        >>> list(skip_list)
        [1, 3]
        """
        node, update_vector = self._locate_node(key)

        if node is not None:
            for i, update_node in enumerate(update_vector):
                if update_node.level > i and update_node.forward[i].key == key:
                    if node.level > i:
                        update_node.forward[i] = node.forward[i]
                    else:
                        update_node.forward = update_node.forward[:i]

    def insert(self, key, value):
        """
        >>> skip_list = SkipList()
        >>> skip_list.insert(2, "Two")
        >>> skip_list.find(2)
        'Two'
        >>> list(skip_list)
        [2]
        """
        node, update_vector = self._locate_node(key)
        if node is not None:
            node.value = value
        else:
            level = self.random_level()

            if level > self.level:
                for _ in range(self.level - 1, level):
                    update_vector.append(self.head)
                self.level = level

            new_node = Node(key, value)

            for i, update_node in enumerate(update_vector[:level]):
                if update_node.level > i:
                    new_node.forward.append(update_node.forward[i])

                if update_node.level < i + 1:
                    update_node.forward.append(new_node)
                else:
                    update_node.forward[i] = new_node

    def find(self, key):
        """
        >>> skip_list = SkipList()
        >>> skip_list.find(2)
        >>> skip_list.insert(2, "Two")
        >>> skip_list.find(2)
        'Two'
        >>> skip_list.insert(2, "Three")
        >>> skip_list.find(2)
        'Three'
        """
        node, _ = self._locate_node(key)

        if node is not None:
            return node.value

        return None


def main():
    """
    >>> pytests()
    """
    skip_list = SkipList()
    skip_list.insert(2, "2")
    skip_list.insert(4, "4")
    skip_list.insert(6, "4")
    skip_list.insert(4, "5")
    skip_list.insert(8, "4")
    skip_list.insert(9, "4")
    skip_list.delete(4)
    print(skip_list)


def pytests():
    for _ in range(100):
        _test_insert()
        _test_insert_overrides_existing_value()
        _test_searching_empty_list_returns_none()
        _test_search()
        _test_deleting_item_from_empty_list_do_nothing()
        _test_deleted_items_are_not_founded_by_find_method()
        _test_delete_removes_only_given_key()
        _test_iter_always_yields_sorted_values()


def _test_insert():
    skip_list = SkipList()
    skip_list.insert("Key1", 3)
    skip_list.insert("Key2", 12)
    skip_list.insert("Key3", 41)
    skip_list.insert("Key4", -19)
    node = skip_list.head
    all_values = {}
    while node.level != 0:
        node = node.forward[0]
        all_values[node.key] = node.value
    assert len(all_values) == 4


def _test_insert_overrides_existing_value():
    skip_list = SkipList()
    skip_list.insert("Key1", 10)
    skip_list.insert("Key1", 12)
    node = skip_list.head
    all_values = {}
    while node.level != 0:
        node = node.forward[0]
        all_values[node.key] = node.value
    assert all_values["Key1"] == 12


def _test_searching_empty_list_returns_none():
    skip_list = SkipList()
    assert skip_list.find("Some key") is None


def _test_search():
    skip_list = SkipList()
    skip_list.insert("Key2", 20)
    assert skip_list.find("Key2") == 20


def _test_deleting_item_from_empty_list_do_nothing():
    skip_list = SkipList()
    skip_list.delete("Some key")
    assert len(skip_list.head.forward) == 0


def _test_deleted_items_are_not_founded_by_find_method():
    skip_list = SkipList()
    skip_list.insert("Key1", 12)
    skip_list.insert("V", 13)
    skip_list.delete("V")
    assert skip_list.find("V") is None


def _test_delete_removes_only_given_key():
    skip_list = SkipList()
    skip_list.insert("Key1", 12)
    skip_list.insert("V", 13)
    skip_list.insert("X", 14)
    skip_list.delete("V")
    assert skip_list.find("V") is None
    assert skip_list.find("X") == 14


def _test_iter_always_yields_sorted_values():
    def is_sorted(lst):
        return all(next_item >= item for item, next_item in pairwise(lst))

    skip_list = SkipList()
    for i in range(10):
        skip_list.insert(i, i)
    assert is_sorted(list(skip_list))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    main()
