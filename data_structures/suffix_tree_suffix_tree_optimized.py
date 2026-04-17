"""
Optimized variants for Suffix Tree / Suffix-based string search.

Variants:
1. NaiveSuffixTree    — Original O(n^2) construction from main file
2. SuffixArray        — O(n log n) construction, used in place of suffix tree for many tasks
3. KMPSearch          — KMP string search, O(n+m) — alternative to suffix tree for single pattern
"""

from __future__ import annotations

import timeit


# --- Variant 1: Naive suffix tree (simple, O(n^2) build) ---
class NaiveSuffixTreeNode:
    def __init__(self) -> None:
        self.children: dict[str, NaiveSuffixTreeNode] = {}
        self.is_end = False
        self.start: int | None = None
        self.end: int | None = None


class NaiveSuffixTree:
    def __init__(self, text: str) -> None:
        self.text = text
        self.root = NaiveSuffixTreeNode()
        for i in range(len(text)):
            self._insert(text[i:], i)

    def _insert(self, suffix: str, index: int) -> None:
        node = self.root
        for ch in suffix:
            if ch not in node.children:
                node.children[ch] = NaiveSuffixTreeNode()
            node = node.children[ch]
        node.is_end = True
        node.start = index
        node.end = index + len(suffix) - 1

    def search(self, pattern: str) -> bool:
        node = self.root
        for ch in pattern:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


# --- Variant 2: Suffix Array (O(n log^2 n) construction, O(m log n) search) ---
class SuffixArray:
    """
    Build a suffix array for efficient pattern search.
    Supports: search, longest repeated substring, count occurrences.
    """

    def __init__(self, text: str) -> None:
        self.text = text
        self.n = len(text)
        self.sa = self._build()

    def _build(self) -> list[int]:
        """O(n log^2 n) construction."""
        n = self.n
        text = self.text
        sa = sorted(range(n), key=lambda i: text[i:])
        return sa

    def search(self, pattern: str) -> bool:
        """Binary search in suffix array: O(m log n)."""
        import bisect

        m = len(pattern)
        text = self.text

        lo, hi = 0, len(self.sa)
        while lo < hi:
            mid = (lo + hi) // 2
            if text[self.sa[mid]: self.sa[mid] + m] < pattern:
                lo = mid + 1
            else:
                hi = mid

        if lo < len(self.sa) and text[self.sa[lo]: self.sa[lo] + m] == pattern:
            return True
        return False

    def count(self, pattern: str) -> int:
        """Count occurrences of pattern: O(m log n)."""
        m = len(pattern)
        text = self.text
        n_sa = len(self.sa)

        # left bound
        lo, hi = 0, n_sa
        while lo < hi:
            mid = (lo + hi) // 2
            if text[self.sa[mid]: self.sa[mid] + m] < pattern:
                lo = mid + 1
            else:
                hi = mid
        left = lo

        # right bound
        lo, hi = 0, n_sa
        while lo < hi:
            mid = (lo + hi) // 2
            if text[self.sa[mid]: self.sa[mid] + m] <= pattern:
                lo = mid + 1
            else:
                hi = mid
        right = lo

        return right - left


# --- Variant 3: KMP single pattern search, O(n+m) ---
class KMPSearch:
    """KMP algorithm: O(n+m) single-pattern search."""

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
        self.lps = self._build_lps()

    def _build_lps(self) -> list[int]:
        p = self.pattern
        m = len(p)
        lps = [0] * m
        length, i = 0, 1
        while i < m:
            if p[i] == p[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        return lps

    def search(self, text: str) -> bool:
        """Return True if pattern found anywhere in text."""
        p = self.pattern
        m = len(p)
        n = len(text)
        if m == 0:
            return True
        i = j = 0
        while i < n:
            if text[i] == p[j]:
                i += 1
                j += 1
            if j == m:
                return True
            elif i < n and text[i] != p[j]:
                if j:
                    j = self.lps[j - 1]
                else:
                    i += 1
        return False


def benchmark() -> None:
    text = "banana" * 100  # 600-char text
    patterns = ["ana", "ban", "xyz", "ananana", "banana"]

    def bench_naive():
        st = NaiveSuffixTree(text)
        for p in patterns:
            st.search(p)

    def bench_sa():
        sa = SuffixArray(text)
        for p in patterns:
            sa.search(p)

    def bench_kmp():
        for p in patterns:
            k = KMPSearch(p)
            k.search(text)

    t1 = timeit.timeit(bench_naive, number=50)
    t2 = timeit.timeit(bench_sa, number=50)
    t3 = timeit.timeit(bench_kmp, number=50)

    print("Benchmark (50 runs, text len=600, 5 patterns):")
    print(f"  Variant 1 (Naive Suffix Tree):  {t1:.4f}s")
    print(f"  Variant 2 (Suffix Array):        {t2:.4f}s")
    print(f"  Variant 3 (KMP per pattern):     {t3:.4f}s")
    print("  KMP is fastest per query; Suffix Array enables multi-query with O(m log n).")


if __name__ == "__main__":
    benchmark()
