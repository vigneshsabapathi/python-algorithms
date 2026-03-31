from typing import Generic, TypeVar

T = TypeVar("T")


class Heap(Generic[T]):
    """
    A generic max-heap implementation.

    Supports build_max_heap and extract_max operations.
    Elements must support comparison operators (e.g. via @total_ordering).

    >>> h = Heap()
    >>> h.build_max_heap([3, 1, 4, 1, 5, 9, 2, 6])
    >>> h.extract_max()
    9
    >>> h.extract_max()
    6
    """

    def __init__(self) -> None:
        self.items: list[T] = []

    def build_max_heap(self, items: list[T]) -> None:
        """Build a max-heap from an unsorted list in O(n) time."""
        self.items = list(items)
        # Start from the last non-leaf node and sift down each node
        for i in range(len(self.items) // 2 - 1, -1, -1):
            self._sift_down(i)

    def extract_max(self) -> T:
        """Remove and return the largest element in O(log n) time."""
        if not self.items:
            raise IndexError("extract_max from empty heap")
        # Swap root (max) with last element, then pop and restore heap property
        self.items[0], self.items[-1] = self.items[-1], self.items[0]
        max_item = self.items.pop()
        if self.items:
            self._sift_down(0)
        return max_item

    def _sift_down(self, index: int) -> None:
        """Push the element at `index` down to its correct position."""
        n = len(self.items)
        while True:
            largest = index
            left = 2 * index + 1
            right = 2 * index + 2

            if left < n and self.items[left] > self.items[largest]:
                largest = left
            if right < n and self.items[right] > self.items[largest]:
                largest = right

            if largest == index:
                break  # already in correct position

            self.items[index], self.items[largest] = self.items[largest], self.items[index]
            index = largest


if __name__ == "__main__":
    import doctest

    doctest.testmod()
