"""
Huffman Coding

https://en.wikipedia.org/wiki/Huffman_coding

Huffman coding is a lossless data compression algorithm. The idea is to
assign variable-length codes to input characters, with shorter codes
assigned to more frequent characters. The result is a prefix-free binary
code (no code is a prefix of another), which allows unambiguous decoding.

The algorithm builds a binary tree (the Huffman tree) bottom-up:
1. Count character frequencies
2. Create leaf nodes for each character
3. Repeatedly merge the two lowest-frequency nodes
4. Traverse the tree to assign bit codes
"""

from __future__ import annotations


class Letter:
    def __init__(self, letter: str, freq: int):
        self.letter: str = letter
        self.freq: int = freq
        self.bitstring: dict[str, str] = {}

    def __repr__(self) -> str:
        return f"{self.letter}:{self.freq}"


class TreeNode:
    def __init__(self, freq: int, left: Letter | TreeNode, right: Letter | TreeNode):
        self.freq: int = freq
        self.left: Letter | TreeNode = left
        self.right: Letter | TreeNode = right


def build_tree(letters: list[Letter]) -> Letter | TreeNode:
    """
    Run through the list of Letters and build the min heap
    for the Huffman Tree.

    >>> letters = [Letter('a', 5), Letter('b', 9), Letter('c', 12)]
    >>> root = build_tree(letters)
    >>> root.freq
    26
    """
    response: list[Letter | TreeNode] = list(letters)
    while len(response) > 1:
        left = response.pop(0)
        right = response.pop(0)
        total_freq = left.freq + right.freq
        node = TreeNode(total_freq, left, right)
        response.append(node)
        response.sort(key=lambda x: x.freq)
    return response[0]


def traverse_tree(root: Letter | TreeNode, bitstring: str) -> list[Letter]:
    """
    Recursively traverse the Huffman Tree to set each
    Letter's bitstring dictionary, and return the list of Letters.

    >>> l = Letter('a', 5)
    >>> traverse_tree(l, "0")
    [a:5]
    >>> l.bitstring
    {'a': '0'}
    """
    if isinstance(root, Letter):
        root.bitstring[root.letter] = bitstring
        return [root]
    treenode: TreeNode = root
    letters = []
    letters += traverse_tree(treenode.left, bitstring + "0")
    letters += traverse_tree(treenode.right, bitstring + "1")
    return letters


def huffman_encode(text: str) -> tuple[str, dict[str, str]]:
    """
    Encode a string using Huffman coding.

    Returns the encoded bitstring and the code table.

    >>> encoded, codes = huffman_encode("aabbc")
    >>> all(c in '01' for c in encoded)
    True
    >>> len(codes) == 3
    True
    >>> huffman_decode(encoded, codes) == "aabbc"
    True
    """
    if not text:
        return "", {}

    # Count frequencies
    freq: dict[str, int] = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1

    # Handle single unique character
    if len(freq) == 1:
        char = next(iter(freq))
        return "0" * len(text), {char: "0"}

    # Build Huffman tree
    letters = sorted(
        [Letter(c, f) for c, f in freq.items()], key=lambda x: x.freq
    )
    root = build_tree(letters)
    letter_list = traverse_tree(root, "")
    codes = {k: v for letter in letter_list for k, v in letter.bitstring.items()}

    # Encode
    encoded = "".join(codes[c] for c in text)
    return encoded, codes


def huffman_decode(encoded: str, codes: dict[str, str]) -> str:
    """
    Decode a Huffman-encoded bitstring using the code table.

    >>> huffman_decode("", {})
    ''
    >>> encoded, codes = huffman_encode("hello world")
    >>> huffman_decode(encoded, codes)
    'hello world'
    """
    if not encoded:
        return ""

    # Reverse the code table: bitstring -> character
    reverse_codes = {v: k for k, v in codes.items()}

    decoded = []
    current = ""
    for bit in encoded:
        current += bit
        if current in reverse_codes:
            decoded.append(reverse_codes[current])
            current = ""
    return "".join(decoded)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
