from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


class SegmentTree:
    def __init__(self, arr: list, fnc: Callable) -> None:
        """
        Segment Tree constructor, it works just with commutative combiner.
        :param arr: list of elements for the segment tree
        :param fnc: commutative function for combine two elements

        >>> SegmentTree(['a', 'b', 'c'], lambda a, b: f'{a}{b}').query(0, 2)
        'abc'
        >>> SegmentTree([(1, 2), (2, 3), (3, 4)],
        ...             lambda a, b: (a[0] + b[0], a[1] + b[1])).query(0, 2)
        (6, 9)
        """
        any_type: Any = None

        self.N: int = len(arr)
        self.st: list = [any_type for _ in range(self.N)] + arr
        self.fn = fnc
        self.build()

    def build(self) -> None:
        for p in range(self.N - 1, 0, -1):
            self.st[p] = self.fn(self.st[p * 2], self.st[p * 2 + 1])

    def update(self, p: int, v: Any) -> None:
        """
        Update an element in log(N) time
        :param p: position to be update
        :param v: new value

        >>> st = SegmentTree([3, 1, 2, 4], min)
        >>> st.query(0, 3)
        1
        >>> st.update(2, -1)
        >>> st.query(0, 3)
        -1
        """
        p += self.N
        self.st[p] = v
        while p > 1:
            p = p // 2
            self.st[p] = self.fn(self.st[p * 2], self.st[p * 2 + 1])

    def query(self, left: int, right: int) -> Any:
        """
        Get range query value in log(N) time
        :param left: left element index
        :param right: right element index
        :return: element combined in the range [left, right]

        >>> st = SegmentTree([1, 2, 3, 4], lambda a, b: a + b)
        >>> st.query(0, 2)
        6
        >>> st.query(1, 2)
        5
        >>> st.query(0, 3)
        10
        >>> st.query(2, 3)
        7
        """
        left, right = left + self.N, right + self.N

        res: Any = None
        while left <= right:
            if left % 2 == 1:
                res = self.st[left] if res is None else self.fn(res, self.st[left])
            if right % 2 == 0:
                res = self.st[right] if res is None else self.fn(res, self.st[right])
            left, right = (left + 1) // 2, (right - 1) // 2
        return res


if __name__ == "__main__":
    import doctest
    from functools import reduce

    doctest.testmod()

    test_array = [1, 10, -2, 9, -3, 8, 4, -7, 5, 6, 11, -12]

    min_segment_tree = SegmentTree(test_array, min)
    max_segment_tree = SegmentTree(test_array, max)
    sum_segment_tree = SegmentTree(test_array, lambda a, b: a + b)

    print("Min query [0,5]:", min_segment_tree.query(0, 5))
    print("Max query [0,5]:", max_segment_tree.query(0, 5))
    print("Sum query [0,5]:", sum_segment_tree.query(0, 5))

    sum_segment_tree.update(2, 100)
    print("Sum query [0,5] after update idx 2 to 100:", sum_segment_tree.query(0, 5))
