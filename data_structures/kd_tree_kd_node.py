#  Created by: Ramy-Badr-Ahmed (https://github.com/Ramy-Badr-Ahmed)
#  Reference: https://github.com/TheAlgorithms/Python/pull/11532

from __future__ import annotations


class KDNode:
    """
    Represents a node in a KD-Tree.

    Attributes:
        point: The point stored in this node.
        left: The left child node.
        right: The right child node.

    >>> node = KDNode([1.0, 2.0])
    >>> node.point
    [1.0, 2.0]
    >>> node.left is None
    True
    >>> node.right is None
    True
    >>> left_child = KDNode([0.5, 1.0])
    >>> right_child = KDNode([2.0, 3.0])
    >>> node2 = KDNode([1.0, 2.0], left=left_child, right=right_child)
    >>> node2.left.point
    [0.5, 1.0]
    >>> node2.right.point
    [2.0, 3.0]
    """

    def __init__(
        self,
        point: list[float],
        left: KDNode | None = None,
        right: KDNode | None = None,
    ) -> None:
        """
        Initializes a KDNode with the given point and child nodes.

        Args:
            point (list[float]): The point stored in this node.
            left (Optional[KDNode]): The left child node.
            right (Optional[KDNode]): The right child node.
        """
        self.point = point
        self.left = left
        self.right = right


if __name__ == "__main__":
    import doctest

    doctest.testmod()
