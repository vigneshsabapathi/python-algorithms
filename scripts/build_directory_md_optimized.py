"""
Optimized directory MD builder with multiple tree-walk strategies.

Improvements over the original:
- pathlib.rglob: Uses Path.rglob("*.py") instead of os.walk — cleaner API,
  handles path joining automatically.
- os.scandir: Uses os.scandir() for faster directory iteration (avoids
  extra stat() calls that os.walk makes internally on some platforms).
- Sorted output with groupby: Groups files by directory using itertools.groupby
  after a single sorted pass, avoiding the dict accumulation pattern.
"""

from __future__ import annotations

import os
from itertools import groupby
from pathlib import Path


# --- Helper functions ---

def to_title(filename: str) -> str:
    """
    Convert snake_case to Title Case.

    >>> to_title("binary_search")
    'Binary Search'
    >>> to_title("quick_sort_3_partition")
    'Quick Sort 3 Partition'
    """
    return filename.replace("_", " ").title()


SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules", ".idea"}
SKIP_FILES = {"__init__.py"}


def _is_valid_py(path: Path, root: Path) -> bool:
    """
    Check if a .py file should be included in the directory listing.

    >>> from pathlib import PurePosixPath as P
    >>> _is_valid_py(P("sorts/bubble.py"), P("."))
    True
    >>> _is_valid_py(P("sorts/__init__.py"), P("."))
    False
    """
    rel = path.relative_to(root) if root != Path(".") else path
    for part in rel.parts[:-1]:
        if part.startswith(".") or part in SKIP_DIRS:
            return False
    if path.name in SKIP_FILES:
        return False
    if path.name.startswith("test_") or path.name.endswith("_test.py"):
        return False
    return True


# --- Strategy 1: os.walk (original) ---

def build_with_os_walk(root: Path) -> str:
    """
    Original os.walk approach with dict grouping.

    >>> import tempfile, os
    >>> tmp = tempfile.mkdtemp()
    >>> os.makedirs(os.path.join(tmp, "sorts"))
    >>> Path(os.path.join(tmp, "sorts", "heap_sort.py")).write_text("pass")
    4
    >>> md = build_with_os_walk(Path(tmp))
    >>> "Heap Sort" in md
    True
    >>> import shutil; shutil.rmtree(tmp)
    """
    groups: dict[str, list[Path]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in sorted(dirnames) if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in sorted(filenames):
            if not fname.endswith(".py"):
                continue
            fpath = Path(dirpath) / fname
            if not _is_valid_py(fpath, root):
                continue
            rel_dir = str(Path(dirpath).relative_to(root))
            key = rel_dir if rel_dir != "." else "root"
            groups.setdefault(key, []).append(fpath)

    lines = ["# DIRECTORY.md", ""]
    for group_name in sorted(groups):
        heading = "Root" if group_name == "root" else to_title(group_name)
        lines.append(f"## {heading}")
        lines.append("")
        for fpath in groups[group_name]:
            rel = fpath.relative_to(root)
            lines.append(f"  * [{to_title(fpath.stem)}]({rel.as_posix()})")
        lines.append("")
    return "\n".join(lines)


# --- Strategy 2: pathlib.rglob ---

def build_with_rglob(root: Path) -> str:
    """
    pathlib.rglob approach — single call collects all .py files.

    >>> import tempfile, os
    >>> tmp = tempfile.mkdtemp()
    >>> os.makedirs(os.path.join(tmp, "sorts"))
    >>> Path(os.path.join(tmp, "sorts", "heap_sort.py")).write_text("pass")
    4
    >>> md = build_with_rglob(Path(tmp))
    >>> "Heap Sort" in md
    True
    >>> import shutil; shutil.rmtree(tmp)
    """
    all_files = sorted(
        f for f in root.rglob("*.py") if _is_valid_py(f, root)
    )

    lines = ["# DIRECTORY.md", ""]
    for dir_key, files in groupby(all_files, key=lambda f: f.parent):
        rel_dir = dir_key.relative_to(root)
        heading = "Root" if str(rel_dir) == "." else to_title(str(rel_dir))
        lines.append(f"## {heading}")
        lines.append("")
        for fpath in files:
            rel = fpath.relative_to(root)
            lines.append(f"  * [{to_title(fpath.stem)}]({rel.as_posix()})")
        lines.append("")
    return "\n".join(lines)


# --- Strategy 3: os.scandir (recursive) ---

def _scandir_py_files(directory: Path, root: Path) -> list[Path]:
    """Recursively collect .py files using os.scandir."""
    results = []
    try:
        entries = sorted(os.scandir(directory), key=lambda e: e.name)
    except PermissionError:
        return results
    for entry in entries:
        if entry.is_dir(follow_symlinks=False):
            if entry.name in SKIP_DIRS or entry.name.startswith("."):
                continue
            results.extend(_scandir_py_files(Path(entry.path), root))
        elif entry.is_file() and entry.name.endswith(".py"):
            fpath = Path(entry.path)
            if _is_valid_py(fpath, root):
                results.append(fpath)
    return results


def build_with_scandir(root: Path) -> str:
    """
    os.scandir approach — faster stat on Windows, explicit recursion.

    >>> import tempfile, os
    >>> tmp = tempfile.mkdtemp()
    >>> os.makedirs(os.path.join(tmp, "sorts"))
    >>> Path(os.path.join(tmp, "sorts", "heap_sort.py")).write_text("pass")
    4
    >>> md = build_with_scandir(Path(tmp))
    >>> "Heap Sort" in md
    True
    >>> import shutil; shutil.rmtree(tmp)
    """
    all_files = _scandir_py_files(root, root)

    lines = ["# DIRECTORY.md", ""]
    for dir_key, files in groupby(all_files, key=lambda f: f.parent):
        rel_dir = dir_key.relative_to(root)
        heading = "Root" if str(rel_dir) == "." else to_title(str(rel_dir))
        lines.append(f"## {heading}")
        lines.append("")
        for fpath in files:
            rel = fpath.relative_to(root)
            lines.append(f"  * [{to_title(fpath.stem)}]({rel.as_posix()})")
        lines.append("")
    return "\n".join(lines)


def benchmark() -> None:
    """Benchmark the three directory-building strategies."""
    import timeit

    root = Path(__file__).resolve().parent.parent
    n = 50

    t_walk = timeit.timeit(lambda: build_with_os_walk(root), number=n)
    t_rglob = timeit.timeit(lambda: build_with_rglob(root), number=n)
    t_scandir = timeit.timeit(lambda: build_with_scandir(root), number=n)

    print(f"Build directory MD ({n} iterations):")
    print(f"  os.walk (original):  {t_walk:.3f}s")
    print(f"  pathlib.rglob:       {t_rglob:.3f}s")
    print(f"  os.scandir:          {t_scandir:.3f}s")

    times = [t_walk, t_rglob, t_scandir]
    names = ["os.walk", "rglob", "scandir"]
    fastest = names[times.index(min(times))]
    print(f"\nFastest: {fastest}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
