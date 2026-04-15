"""
Build a Markdown directory listing from the repository structure.

Walks the project tree and generates a DIRECTORY.md file with nested bullet
lists linking to every Python file. Used by TheAlgorithms/Python to auto-generate
the repo's table of contents.

Source: https://github.com/TheAlgorithms/Python/blob/master/scripts/build_directory_md.py
"""

from __future__ import annotations

import os
from pathlib import Path


def to_title(filename: str) -> str:
    """
    Convert a snake_case filename (without extension) to Title Case.

    >>> to_title("binary_search")
    'Binary Search'
    >>> to_title("hello_world_test")
    'Hello World Test'
    >>> to_title("single")
    'Single'
    >>> to_title("")
    ''
    >>> to_title("already")
    'Already'
    """
    return filename.replace("_", " ").title()


def make_link(filepath: Path, root: Path) -> str:
    """
    Create a Markdown link for a file relative to the root directory.

    >>> from pathlib import PurePosixPath as P
    >>> make_link(P("sorts/bubble_sort.py"), P("."))
    '[Bubble Sort](sorts/bubble_sort.py)'
    >>> make_link(P("strings/anagrams.py"), P("."))
    '[Anagrams](strings/anagrams.py)'
    >>> make_link(P("deep/nested/algo.py"), P("."))
    '[Algo](deep/nested/algo.py)'
    """
    relative = filepath.relative_to(root) if root != Path(".") else filepath
    title = to_title(filepath.stem)
    return f"[{title}]({relative.as_posix()})"


def should_include(path: Path) -> bool:
    """
    Determine whether a file/directory should appear in the listing.

    Excludes hidden dirs, __pycache__, venv, .git, __init__.py, and test files.

    >>> should_include(Path("sorts/bubble_sort.py"))
    True
    >>> should_include(Path(".git/config"))
    False
    >>> should_include(Path("__pycache__/mod.pyc"))
    False
    >>> should_include(Path("sorts/__init__.py"))
    False
    >>> should_include(Path("venv/lib/site.py"))
    False
    >>> should_include(Path("tests/test_sort.py"))
    False
    """
    parts = path.parts
    excluded_dirs = {".git", "__pycache__", "venv", ".venv", "node_modules", ".idea"}
    for part in parts:
        if part.startswith(".") and part != ".":
            return False
        if part in excluded_dirs:
            return False
    if path.name == "__init__.py":
        return False
    if path.name.startswith("test_") or path.name.endswith("_test.py"):
        return False
    return True


def collect_python_files(root: Path) -> dict[str, list[Path]]:
    """
    Collect all Python files grouped by their parent directory.

    Returns a dict mapping directory name -> sorted list of .py file paths.

    >>> import tempfile, os
    >>> tmp = tempfile.mkdtemp()
    >>> os.makedirs(os.path.join(tmp, "sorts"))
    >>> Path(os.path.join(tmp, "sorts", "bubble.py")).write_text("pass")
    4
    >>> Path(os.path.join(tmp, "sorts", "__init__.py")).write_text("")
    0
    >>> Path(os.path.join(tmp, "main.py")).write_text("pass")
    4
    >>> result = collect_python_files(Path(tmp))
    >>> sorted(result.keys())
    ['root', 'sorts']
    >>> import shutil; shutil.rmtree(tmp)
    """
    groups: dict[str, list[Path]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in sorted(dirnames)
            if not d.startswith(".") and d not in {"__pycache__", "venv", ".venv"}
        ]
        for fname in sorted(filenames):
            if not fname.endswith(".py"):
                continue
            fpath = Path(dirpath) / fname
            if not should_include(fpath.relative_to(root)):
                continue
            rel_dir = Path(dirpath).relative_to(root)
            key = str(rel_dir) if str(rel_dir) != "." else "root"
            groups.setdefault(key, []).append(fpath)
    return groups


def build_markdown(root: Path) -> str:
    """
    Build the complete Markdown directory listing.

    >>> import tempfile, os
    >>> tmp = tempfile.mkdtemp()
    >>> os.makedirs(os.path.join(tmp, "sorts"))
    >>> Path(os.path.join(tmp, "sorts", "bubble_sort.py")).write_text("pass")
    4
    >>> md = build_markdown(Path(tmp))
    >>> "## Sorts" in md
    True
    >>> "Bubble Sort" in md
    True
    >>> import shutil; shutil.rmtree(tmp)
    """
    groups = collect_python_files(root)
    lines = ["# DIRECTORY.md", "", "Auto-generated listing of all algorithms.", ""]

    for group_name in sorted(groups):
        if group_name == "root":
            lines.append("## Root")
        else:
            lines.append(f"## {to_title(group_name)}")
        lines.append("")
        for fpath in groups[group_name]:
            link = make_link(fpath, root)
            lines.append(f"  * {link}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- build_directory_md demo ---")
    root = Path(__file__).resolve().parent.parent
    md = build_markdown(root)
    print(md[:500])
    print(f"\n... ({len(md)} chars total)")
