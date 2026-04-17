from __future__ import annotations


class SuffixTreeNode:
    """
    A node in a Suffix Tree.

    Attributes:
        children: Mapping from character to child SuffixTreeNode.
        is_end_of_string: True if this node marks the end of a suffix.
        start: Start index of the suffix in the original text.
        end: End index of the suffix in the original text.
        suffix_link: Link to another suffix tree node (Ukkonen's algorithm).

    >>> node = SuffixTreeNode()
    >>> node.is_end_of_string
    False
    >>> node.start is None
    True
    >>> node.end is None
    True
    >>> node.children
    {}
    >>> child = SuffixTreeNode(is_end_of_string=True, start=0, end=4)
    >>> child.is_end_of_string
    True
    >>> child.start
    0
    >>> child.end
    4
    """

    def __init__(
        self,
        children: dict[str, SuffixTreeNode] | None = None,
        is_end_of_string: bool = False,
        start: int | None = None,
        end: int | None = None,
        suffix_link: SuffixTreeNode | None = None,
    ) -> None:
        """
        Initializes a suffix tree node.

        Parameters:
            children: The children of this node.
            is_end_of_string: Indicates if this node represents
                              the end of a string.
            start: The start index of the suffix in the text.
            end: The end index of the suffix in the text.
            suffix_link: Link to another suffix tree node.
        """
        self.children = children or {}
        self.is_end_of_string = is_end_of_string
        self.start = start
        self.end = end
        self.suffix_link = suffix_link


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    node = SuffixTreeNode()
    print(f"Empty node: children={node.children}, is_end={node.is_end_of_string}")
    child = SuffixTreeNode(is_end_of_string=True, start=0, end=4)
    print(f"Leaf node: start={child.start}, end={child.end}")
