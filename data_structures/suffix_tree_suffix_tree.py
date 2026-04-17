from __future__ import annotations

try:
    from data_structures.suffix_tree_suffix_tree_node import SuffixTreeNode
except ModuleNotFoundError:
    from suffix_tree_suffix_tree_node import SuffixTreeNode  # type: ignore[no-redef]


class SuffixTree:
    """
    A Suffix Tree data structure that enables O(m) pattern search
    in a text of length n (after O(n) or O(n^2) construction).

    This naive implementation builds in O(n^2) by inserting all suffixes.

    >>> st = SuffixTree("banana")
    >>> st.search("ana")
    True
    >>> st.search("ban")
    True
    >>> st.search("xyz")
    False
    >>> st.search("")
    True
    >>> st2 = SuffixTree("mississippi")
    >>> st2.search("issi")
    True
    >>> st2.search("ippi")
    True
    >>> st2.search("xyz")
    False
    """

    def __init__(self, text: str) -> None:
        """
        Initializes the suffix tree with the given text.

        Args:
            text (str): The text for which the suffix tree is to be built.
        """
        self.text: str = text
        self.root: SuffixTreeNode = SuffixTreeNode()
        self.build_suffix_tree()

    def build_suffix_tree(self) -> None:
        """
        Builds the suffix tree for the given text by adding all suffixes.
        """
        text = self.text
        n = len(text)
        for i in range(n):
            suffix = text[i:]
            self._add_suffix(suffix, i)

    def _add_suffix(self, suffix: str, index: int) -> None:
        """
        Adds a suffix to the suffix tree.

        Args:
            suffix (str): The suffix to add.
            index (int): The starting index of the suffix in the original text.
        """
        node = self.root
        for char in suffix:
            if char not in node.children:
                node.children[char] = SuffixTreeNode()
            node = node.children[char]
        node.is_end_of_string = True
        node.start = index
        node.end = index + len(suffix) - 1

    def search(self, pattern: str) -> bool:
        """
        Searches for a pattern in the suffix tree.

        Args:
            pattern (str): The pattern to search for.

        Returns:
            bool: True if the pattern is found, False otherwise.

        >>> st = SuffixTree("hello")
        >>> st.search("ell")
        True
        >>> st.search("world")
        False
        """
        node = self.root
        for char in pattern:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    text = "banana"
    st = SuffixTree(text)
    patterns = ["ana", "ban", "nan", "xyz", "a", "banana"]
    for p in patterns:
        print(f"  '{p}' in '{text}': {st.search(p)}")
