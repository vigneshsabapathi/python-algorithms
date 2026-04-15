"""
Validate Python filenames in the repository follow naming conventions.

Rules enforced:
- All .py filenames must be snake_case (lowercase + underscores only).
- No spaces, hyphens, or uppercase letters in filenames.
- __init__.py is always allowed.
- Directories must also be snake_case.

Source: https://github.com/TheAlgorithms/Python/blob/master/scripts/validate_filenames.py
"""

from __future__ import annotations

import os
import re
from pathlib import Path


SNAKE_CASE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
ALLOWED_FILES = {"__init__.py", "README.md", ".gitignore", ".gitkeep"}


def is_snake_case(name: str) -> bool:
    """
    Check if a name follows snake_case convention.

    >>> is_snake_case("bubble_sort")
    True
    >>> is_snake_case("binary_search")
    True
    >>> is_snake_case("a")
    True
    >>> is_snake_case("BubbleSort")
    False
    >>> is_snake_case("bubble-sort")
    False
    >>> is_snake_case("bubble sort")
    False
    >>> is_snake_case("1_starts_with_digit")
    False
    >>> is_snake_case("")
    False
    >>> is_snake_case("__init__")
    False
    >>> is_snake_case("my_file_2")
    True
    """
    return bool(SNAKE_CASE_RE.match(name))


def validate_python_filename(filename: str) -> tuple[bool, str]:
    """
    Validate a single Python filename.

    Returns (is_valid, reason).

    >>> validate_python_filename("bubble_sort.py")
    (True, 'valid snake_case')
    >>> validate_python_filename("__init__.py")
    (True, 'allowed special file')
    >>> validate_python_filename("BubbleSort.py")
    (False, 'not snake_case: BubbleSort')
    >>> validate_python_filename("my-algo.py")
    (False, 'not snake_case: my-algo')
    >>> validate_python_filename("readme.txt")
    (True, 'not a Python file')
    >>> validate_python_filename("test.PY")
    (False, 'not snake_case: test.PY')
    """
    if filename in ALLOWED_FILES:
        return True, "allowed special file"
    if not filename.endswith(".py"):
        if filename.upper().endswith(".PY"):
            stem = filename[:-3] if len(filename) > 3 else filename
            return False, f"not snake_case: {filename}"
        return True, "not a Python file"
    stem = filename[:-3]  # remove .py
    if is_snake_case(stem):
        return True, "valid snake_case"
    return False, f"not snake_case: {stem}"


def validate_directory_name(dirname: str) -> tuple[bool, str]:
    """
    Validate a directory name follows snake_case convention.

    >>> validate_directory_name("sorts")
    (True, 'valid snake_case')
    >>> validate_directory_name("bit_manipulation")
    (True, 'valid snake_case')
    >>> validate_directory_name("MyFolder")
    (False, 'not snake_case: MyFolder')
    >>> validate_directory_name(".git")
    (True, 'hidden directory (skipped)')
    >>> validate_directory_name("__pycache__")
    (True, 'system directory (skipped)')
    """
    if dirname.startswith("."):
        return True, "hidden directory (skipped)"
    if dirname.startswith("__") and dirname.endswith("__"):
        return True, "system directory (skipped)"
    if is_snake_case(dirname):
        return True, "valid snake_case"
    return False, f"not snake_case: {dirname}"


def scan_repository(root: Path) -> list[dict]:
    """
    Scan the repo and return a list of validation issues.

    Each issue is a dict with keys: path, kind ('file' or 'dir'), reason.

    >>> import tempfile, os
    >>> tmp = tempfile.mkdtemp()
    >>> os.makedirs(os.path.join(tmp, "GoodDir"))
    >>> Path(os.path.join(tmp, "GoodDir", "Bad-File.py")).write_text("pass")
    4
    >>> issues = scan_repository(Path(tmp))
    >>> len(issues)
    2
    >>> issues[0]["kind"]
    'dir'
    >>> issues[1]["kind"]
    'file'
    >>> import shutil; shutil.rmtree(tmp)
    """
    issues = []
    skip_dirs = {".git", "__pycache__", "venv", ".venv", "node_modules"}

    for dirpath, dirnames, filenames in os.walk(root):
        # Validate directory names
        rel_dir = Path(dirpath).relative_to(root)
        if str(rel_dir) != ".":
            dirname = Path(dirpath).name
            if dirname not in skip_dirs:
                valid, reason = validate_directory_name(dirname)
                if not valid:
                    issues.append({
                        "path": str(rel_dir),
                        "kind": "dir",
                        "reason": reason,
                    })

        # Prune excluded directories
        dirnames[:] = [d for d in sorted(dirnames) if d not in skip_dirs]

        # Validate filenames
        for fname in sorted(filenames):
            valid, reason = validate_python_filename(fname)
            if not valid:
                issues.append({
                    "path": str(rel_dir / fname),
                    "kind": "file",
                    "reason": reason,
                })

    return issues


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- validate_filenames demo ---")
    root = Path(__file__).resolve().parent.parent
    issues = scan_repository(root)
    if issues:
        print(f"Found {len(issues)} naming issues:")
        for issue in issues:
            print(f"  [{issue['kind']}] {issue['path']}: {issue['reason']}")
    else:
        print("All filenames follow snake_case convention.")
