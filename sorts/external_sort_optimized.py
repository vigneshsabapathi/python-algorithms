"""
External sort — fixed and optimized for interview prep.

External sort handles datasets larger than available RAM by splitting the
input into sorted "run" files (each fits in memory), then merging them.
Classic algorithm used in databases, MapReduce, and OS file utilities.

Bugs fixed from the original:
  1. NWayMerge.select() never updated min_str → always returned last index
     (silent correctness bug: merged output was not sorted)
  2. buffer_size used / (float division) instead of // (integer) →
     TypeError when passed to open() as buffering argument
  3. FileSplitter.cleanup() used map() (lazy in Python 3) → temp files
     were never deleted (resource leak)

Optimization:
  heapq.merge replaces the O(k) linear select() with O(log k) heap merge.
  For k sorted runs, total merge cost drops from O(n·k) to O(n·log k).
"""

from __future__ import annotations

import heapq
import os
import tempfile
from typing import Callable


class ExternalSortFixed:
    """
    External sort with all original bugs fixed.
    Uses the corrected NWayMerge.select() (updates min_str) and
    integer buffer sizing. Drops the map() cleanup bug.
    """

    BLOCK_FMT = "block_{}.dat"

    def __init__(self, block_size: int = 1024 * 1024):
        self.block_size = block_size

    def sort(self, filename: str, sort_key: Callable | None = None) -> str:
        """Sort *filename* into *filename*.out. Returns output path."""
        block_files = self._split(filename, sort_key)
        outpath = filename + ".out"
        num_blocks = len(block_files)
        # Fix #2: integer division for buffer_size
        buf = max(1, self.block_size // (num_blocks + 1))
        self._merge(block_files, outpath, buf)
        # Fix #3: explicit loop instead of lazy map()
        for f in block_files:
            os.remove(f)
        return outpath

    def _split(self, filename: str, sort_key: Callable | None) -> list[str]:
        block_files = []
        i = 0
        with open(filename) as fh:
            while True:
                lines = fh.readlines(self.block_size)
                if not lines:
                    break
                lines.sort(key=sort_key)
                path = self.BLOCK_FMT.format(i)
                with open(path, "w") as bf:
                    bf.write("".join(lines))
                block_files.append(path)
                i += 1
        return block_files

    def _merge(self, block_files: list[str], outpath: str, buf: int) -> None:
        handles = [open(f, "r", buf) for f in block_files]  # noqa: UP015
        with open(outpath, "w", buf) as out:
            # Fix #1: corrected linear select (updates min_str)
            buffers: dict[int, str | None] = {i: None for i in range(len(handles))}
            empty: set[int] = set()

            def refresh() -> bool:
                for i in range(len(handles)):
                    if buffers[i] is None and i not in empty:
                        line = handles[i].readline()
                        if line == "":
                            empty.add(i)
                            handles[i].close()
                        else:
                            buffers[i] = line
                return len(empty) < len(handles)

            while refresh():
                active = {i: v for i, v in buffers.items()
                          if i not in empty and v is not None}
                # Fixed select: update min_str on each better candidate
                min_idx = -1
                min_val = None
                for idx, val in active.items():
                    if min_val is None or val < min_val:
                        min_idx = idx
                        min_val = val
                if min_idx >= 0:
                    out.write(buffers[min_idx])  # type: ignore[arg-type]
                    buffers[min_idx] = None


class ExternalSortHeap:
    """
    External sort using heapq.merge for O(n log k) N-way merge.

    heapq.merge maintains a k-element min-heap: each pop is O(log k)
    instead of O(k) for the linear scan. For large k (many runs) this
    is significantly faster.

    For n total lines and k runs:
      Linear select merge: O(n * k)
      heapq.merge:         O(n * log k)
    """

    def __init__(self, block_size: int = 1024 * 1024):
        self.block_size = block_size

    def sort(self, filename: str, sort_key: Callable | None = None) -> str:
        """Sort *filename* into *filename*.heap.out. Returns output path."""
        block_files = self._split(filename, sort_key)
        outpath = filename + ".heap.out"
        self._merge(block_files, outpath)
        for f in block_files:
            os.remove(f)
        return outpath

    def _split(self, filename: str, sort_key: Callable | None) -> list[str]:
        block_files = []
        i = 0
        with open(filename) as fh:
            while True:
                lines = fh.readlines(self.block_size)
                if not lines:
                    break
                lines.sort(key=sort_key)
                fd, path = tempfile.mkstemp(suffix=f"_block{i}.dat", text=True)
                with os.fdopen(fd, "w") as bf:
                    bf.writelines(lines)
                block_files.append(path)
                i += 1
        return block_files

    def _merge(self, block_files: list[str], outpath: str) -> None:
        handles = [open(f) for f in block_files]
        with open(outpath, "w") as out:
            # heapq.merge lazily merges k sorted iterables in O(n log k)
            out.writelines(heapq.merge(*handles))
        for h in handles:
            h.close()


def demo() -> None:
    """End-to-end demo: sort a 500-line file in 100-byte blocks (many runs)."""
    import random, timeit

    lines = [f"{random.randint(0, 9999):06d} line_{i:04d}\n" for i in range(500)]
    random.shuffle(lines)

    # Write temp input file
    fd, inpath = tempfile.mkstemp(suffix=".txt", text=True)
    with os.fdopen(fd, "w") as f:
        f.writelines(lines)

    expected = sorted(lines)

    # ── Fixed (linear select) ─────────────────────────────────────────
    fixed = ExternalSortFixed(block_size=200)
    out_fixed = fixed.sort(inpath)
    with open(out_fixed) as f:
        result_fixed = f.readlines()
    os.remove(out_fixed)
    print(f"ExternalSortFixed  correct: {result_fixed == expected}")

    # ── Heap merge ───────────────────────────────────────────────────
    heap = ExternalSortHeap(block_size=200)
    out_heap = heap.sort(inpath)
    with open(out_heap) as f:
        result_heap = f.readlines()
    os.remove(out_heap)
    print(f"ExternalSortHeap   correct: {result_heap == expected}")

    # ── Timing (larger file, 3000 lines) ────────────────────────────
    print()
    big_lines = [f"{random.randint(0, 99999):08d}\n" for _ in range(3000)]
    random.shuffle(big_lines)
    fd2, inpath2 = tempfile.mkstemp(suffix=".txt", text=True)
    with os.fdopen(fd2, "w") as f:
        f.writelines(big_lines)

    n_runs = 10

    def run_fixed():
        s = ExternalSortFixed(block_size=1000)
        p = s.sort(inpath2)
        os.remove(p)

    def run_heap():
        s = ExternalSortHeap(block_size=1000)
        p = s.sort(inpath2)
        os.remove(p)

    t_fixed = timeit.timeit(run_fixed, number=n_runs)
    t_heap  = timeit.timeit(run_heap,  number=n_runs)
    print(f"3000-line file, block=1000B ({n_runs} runs):")
    print(f"  fixed (linear select): {t_fixed:.3f}s")
    print(f"  heap  (heapq.merge):   {t_heap:.3f}s")

    # Cleanup
    os.remove(inpath)
    os.remove(inpath2)


if __name__ == "__main__":
    demo()
