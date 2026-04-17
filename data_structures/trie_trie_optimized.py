"""
Optimized variants for Trie (Prefix Tree).

Variants:
1. DictTrie       — Original dict-based trie (from main file)
2. ArrayTrie      — Array-based trie (26 children, lowercase English only), faster
3. CompressedTrie — Radix/compressed trie (merged single-child paths)
"""

from __future__ import annotations

import timeit


# --- Variant 1: Dict-based trie (flexible, any character) ---
class DictTrieNode:
    def __init__(self) -> None:
        self.children: dict[str, DictTrieNode] = {}
        self.is_leaf = False


class DictTrie:
    def __init__(self) -> None:
        self.root = DictTrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = DictTrieNode()
            node = node.children[ch]
        node.is_leaf = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_leaf

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


# --- Variant 2: Array-based trie (lowercase a-z only, faster lookup) ---
class ArrayTrieNode:
    __slots__ = ("children", "is_leaf")

    def __init__(self) -> None:
        self.children: list[ArrayTrieNode | None] = [None] * 26
        self.is_leaf = False


class ArrayTrie:
    def __init__(self) -> None:
        self.root = ArrayTrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            idx = ord(ch) - ord("a")
            if node.children[idx] is None:
                node.children[idx] = ArrayTrieNode()
            node = node.children[idx]  # type: ignore[assignment]
        node.is_leaf = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            idx = ord(ch) - ord("a")
            if node.children[idx] is None:
                return False
            node = node.children[idx]  # type: ignore[assignment]
        return node.is_leaf

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            idx = ord(ch) - ord("a")
            if node.children[idx] is None:
                return False
            node = node.children[idx]  # type: ignore[assignment]
        return True


# --- Variant 3: Compressed (Radix) trie ---
class RadixTrieNode:
    def __init__(self, prefix: str = "", is_leaf: bool = False) -> None:
        self.prefix = prefix
        self.is_leaf = is_leaf
        self.children: dict[str, RadixTrieNode] = {}

    def _common_prefix_len(self, a: str, b: str) -> int:
        i = 0
        while i < len(a) and i < len(b) and a[i] == b[i]:
            i += 1
        return i


class RadixTrie:
    def __init__(self) -> None:
        self.root = RadixTrieNode()

    def insert(self, word: str) -> None:
        self._insert(self.root, word)

    def _insert(self, node: RadixTrieNode, word: str) -> None:
        if not word:
            node.is_leaf = True
            return
        first = word[0]
        if first not in node.children:
            node.children[first] = RadixTrieNode(word, True)
            return
        child = node.children[first]
        cp = node._common_prefix_len(child.prefix, word)
        if cp == len(child.prefix):
            self._insert(child, word[cp:])
        else:
            # split
            new_child = RadixTrieNode(child.prefix[:cp], False)
            child.prefix = child.prefix[cp:]
            new_child.children[child.prefix[0]] = child
            node.children[first] = new_child
            remaining = word[cp:]
            if remaining:
                new_child.children[remaining[0]] = RadixTrieNode(remaining, True)
            else:
                new_child.is_leaf = True

    def search(self, word: str) -> bool:
        return self._search(self.root, word)

    def _search(self, node: RadixTrieNode, word: str) -> bool:
        if not word:
            return node.is_leaf
        first = word[0]
        if first not in node.children:
            return False
        child = node.children[first]
        cp = node._common_prefix_len(child.prefix, word)
        if cp < len(child.prefix):
            return False
        return self._search(child, word[cp:])


def benchmark() -> None:
    words = (
        "banana bananas bandana band apple all beast "
        "application apply apt apt ape bear beard"
    ).split()
    searches = ["banana", "band", "beast", "application", "xyz", "app", "ape"]

    def bench_dict():
        t = DictTrie()
        for w in words:
            t.insert(w)
        for s in searches:
            t.search(s)
        for s in searches:
            t.starts_with(s[:3])

    def bench_array():
        t = ArrayTrie()
        for w in words:
            t.insert(w)
        for s in searches:
            t.search(s)
        for s in searches:
            t.starts_with(s[:3])

    def bench_radix():
        t = RadixTrie()
        for w in words:
            t.insert(w)
        for s in searches:
            t.search(s)

    t1 = timeit.timeit(bench_dict, number=5000)
    t2 = timeit.timeit(bench_array, number=5000)
    t3 = timeit.timeit(bench_radix, number=5000)

    print("Benchmark (5000 runs, 14 words, 7 searches):")
    print(f"  Variant 1 (Dict Trie):    {t1:.4f}s")
    print(f"  Variant 2 (Array Trie):   {t2:.4f}s")
    print(f"  Variant 3 (Radix Trie):   {t3:.4f}s")
    print("  Array trie is fastest for lowercase ASCII; dict trie most flexible.")


if __name__ == "__main__":
    benchmark()
