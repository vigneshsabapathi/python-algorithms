"""Queue represented by a pseudo stack (represented by a list with pop and append)."""

from typing import Any


class Queue:
    def __init__(self):
        self.stack = []
        self.length = 0

    def __str__(self):
        printed = "<" + str(self.stack)[1:-1] + ">"
        return printed

    def put(self, item: Any) -> None:
        """
        Enqueues item.

        >>> q = Queue()
        >>> q.put(1)
        >>> q.put(2)
        >>> q.put(3)
        >>> str(q)
        '<1, 2, 3>'
        >>> q.size()
        3
        """
        self.stack.append(item)
        self.length = self.length + 1

    def get(self) -> Any:
        """
        Dequeues and returns item.

        >>> q = Queue()
        >>> q.put(1)
        >>> q.put(2)
        >>> q.get()
        1
        >>> q.get()
        2
        """
        self.rotate(1)
        dequeued = self.stack[self.length - 1]
        self.stack = self.stack[:-1]
        self.rotate(self.length - 1)
        self.length = self.length - 1
        return dequeued

    def rotate(self, rotation: int) -> None:
        """
        Rotates the queue rotation times.
        """
        for _ in range(rotation):
            temp = self.stack[0]
            self.stack = self.stack[1:]
            self.put(temp)
            self.length = self.length - 1

    def front(self) -> Any:
        """
        Reports item at the front of the queue.

        >>> q = Queue()
        >>> q.put(10)
        >>> q.put(20)
        >>> q.front()
        10
        """
        front = self.get()
        self.put(front)
        self.rotate(self.length - 1)
        return front

    def size(self) -> int:
        """Returns the length of the queue.

        >>> q = Queue()
        >>> q.size()
        0
        >>> q.put(1)
        >>> q.size()
        1
        """
        return self.length


if __name__ == "__main__":
    import doctest

    doctest.testmod()
