"""
Optimized Trie-based autocomplete.

Improvements over the original:
- Dedicated TrieNode with an `is_end` bool instead of a `"#"` sentinel key
- Clean word output (no trailing space artifact from the sentinel)
- Iterative DFS via an explicit stack — no recursion limit risk for long words
- `autocomplete` is a Trie method, not a module-level function that captures
  a global trie
- `insert` accepts an iterable of words for convenience
"""

from __future__ import annotations


class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}
        self.is_end: bool = False


class Trie:
    def __init__(self) -> None:
        self._root = TrieNode()

    def insert_word(self, word: str) -> None:
        node = self._root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def insert(self, words: list[str]) -> None:
        for word in words:
            self.insert_word(word)

    def autocomplete(self, prefix: str) -> tuple[str, ...]:
        """
        Return all words in the trie that start with *prefix*.

        Uses an iterative DFS stack — safe for arbitrarily long words.

        >>> t = Trie()
        >>> t.insert(["depart", "detergent", "daring", "dog", "deer", "deal"])
        >>> sorted(t.autocomplete("de"))
        ['deal', 'deer', 'depart', 'detergent']
        >>> t.autocomplete("da")
        ('daring',)
        >>> t.autocomplete("dog")
        ('dog',)
        >>> t.autocomplete("xyz")
        ()
        >>> sorted(t.autocomplete(""))
        ['daring', 'deal', 'deer', 'depart', 'detergent', 'dog']
        """
        node = self._root
        for char in prefix:
            if char not in node.children:
                return ()
            node = node.children[char]

        # Iterative DFS: stack holds (node, suffix_built_so_far)
        results: list[str] = []
        stack: list[tuple[TrieNode, str]] = [(node, prefix)]
        while stack:
            current, word_so_far = stack.pop()
            if current.is_end:
                results.append(word_so_far)
            for char, child in current.children.items():
                stack.append((child, word_so_far + char))

        return tuple(results)


def benchmark() -> None:
    import timeit

    from strings.autocomplete_using_trie import (
        Trie as OrigTrie,
        autocomplete_using_trie,
        words,
    )

    word_list = list(words)
    n = 100_000

    def orig_setup() -> None:
        t = OrigTrie()
        for w in word_list:
            t.insert_word(w)

    def opt_setup() -> None:
        t = Trie()
        t.insert(word_list)

    orig_insert = timeit.timeit(orig_setup, number=n)
    opt_insert = timeit.timeit(opt_setup, number=n)

    # Build once, benchmark autocomplete
    orig_trie = OrigTrie()
    for w in word_list:
        orig_trie.insert_word(w)
    opt_trie = Trie()
    opt_trie.insert(word_list)

    orig_ac = timeit.timeit(lambda: autocomplete_using_trie("de"), number=n)
    opt_ac = timeit.timeit(lambda: opt_trie.autocomplete("de"), number=n)

    print(f"insert ({len(word_list)} words) — original: {orig_insert:.3f}s  optimized: {opt_insert:.3f}s")
    print(f"autocomplete('de')         — original: {orig_ac:.3f}s  optimized: {opt_ac:.3f}s")

    print(f"\nFastest insert:       {'optimized' if opt_insert < orig_insert else 'original'}")
    print(f"Fastest autocomplete: {'optimized' if opt_ac < orig_ac else 'original'}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
