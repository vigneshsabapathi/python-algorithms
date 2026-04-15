"""
Optimized filename validator with multiple regex/matching strategies.

Improvements over the original:
- Compiled regex with fullmatch: Uses re.fullmatch() instead of re.match(),
  avoiding the need for end-of-string anchor.
- Set-based character validation: Checks each character against a frozenset
  of allowed characters — avoids regex overhead entirely.
- str.isidentifier + lower check: Leverages Python's built-in identifier
  validation combined with a lowercase check.
"""

from __future__ import annotations

import os
import re
import string
from pathlib import Path


# --- snake_case validation strategies ---

_SNAKE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_SNAKE_FULLMATCH_RE = re.compile(r"[a-z][a-z0-9_]*")
_ALLOWED_CHARS = frozenset(string.ascii_lowercase + string.digits + "_")


def is_snake_regex_match(name: str) -> bool:
    """
    Original: re.match with anchored pattern.

    >>> is_snake_regex_match("bubble_sort")
    True
    >>> is_snake_regex_match("BubbleSort")
    False
    >>> is_snake_regex_match("")
    False
    >>> is_snake_regex_match("a1_b2")
    True
    """
    return bool(_SNAKE_RE.match(name))


def is_snake_regex_fullmatch(name: str) -> bool:
    """
    re.fullmatch — no anchors needed in the pattern.

    >>> is_snake_regex_fullmatch("bubble_sort")
    True
    >>> is_snake_regex_fullmatch("BubbleSort")
    False
    >>> is_snake_regex_fullmatch("")
    False
    """
    return bool(_SNAKE_FULLMATCH_RE.fullmatch(name))


def is_snake_set_check(name: str) -> bool:
    """
    Frozenset membership check — no regex at all.

    >>> is_snake_set_check("bubble_sort")
    True
    >>> is_snake_set_check("BubbleSort")
    False
    >>> is_snake_set_check("")
    False
    >>> is_snake_set_check("1bad")
    False
    >>> is_snake_set_check("good_2")
    True
    """
    if not name or not name[0].islower():
        return False
    return all(c in _ALLOWED_CHARS for c in name)


def is_snake_builtin(name: str) -> bool:
    """
    str.isidentifier + lowercase check — uses CPython's internal validator.

    >>> is_snake_builtin("bubble_sort")
    True
    >>> is_snake_builtin("BubbleSort")
    False
    >>> is_snake_builtin("")
    False
    >>> is_snake_builtin("_private")
    False
    >>> is_snake_builtin("class")
    True
    """
    if not name or not name[0].islower():
        return False
    # isidentifier allows uppercase too, so we also check islower
    # But digits aren't "lower", so we check: all alphanumeric chars are lowercase
    return name.isidentifier() and name.replace("_", "").replace(
        "0", "").replace("1", "").replace("2", "").replace("3", "").replace(
        "4", "").replace("5", "").replace("6", "").replace("7", "").replace(
        "8", "").replace("9", "").islower()


def validate_and_scan(root: Path, strategy: str = "regex_match") -> list[dict]:
    """
    Scan repo using the specified snake_case checker.

    strategy: 'regex_match' | 'regex_fullmatch' | 'set_check' | 'builtin'
    """
    checkers = {
        "regex_match": is_snake_regex_match,
        "regex_fullmatch": is_snake_regex_fullmatch,
        "set_check": is_snake_set_check,
        "builtin": is_snake_builtin,
    }
    check = checkers[strategy]
    skip_dirs = {".git", "__pycache__", "venv", ".venv", "node_modules"}
    allowed_files = {"__init__.py", "README.md", ".gitignore"}
    issues = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in sorted(dirnames) if d not in skip_dirs]
        dirname = Path(dirpath).name
        if str(Path(dirpath).relative_to(root)) != "." and dirname not in skip_dirs:
            if not dirname.startswith(".") and not check(dirname):
                issues.append({
                    "path": str(Path(dirpath).relative_to(root)),
                    "kind": "dir",
                    "reason": f"not snake_case: {dirname}",
                })
        for fname in sorted(filenames):
            if fname in allowed_files or not fname.endswith(".py"):
                continue
            stem = fname[:-3]
            if not check(stem):
                issues.append({
                    "path": str(Path(dirpath).relative_to(root) / fname),
                    "kind": "file",
                    "reason": f"not snake_case: {stem}",
                })
    return issues


def benchmark() -> None:
    """Benchmark snake_case validation strategies."""
    import timeit

    test_names = [
        "bubble_sort", "binary_search", "quick_sort_3_partition",
        "BubbleSort", "my-algo", "good_name_2", "a", "1bad",
        "really_long_algorithm_name_here", "x",
    ]
    n = 500_000

    t_match = timeit.timeit(
        lambda: [is_snake_regex_match(name) for name in test_names], number=n
    )
    t_fullmatch = timeit.timeit(
        lambda: [is_snake_regex_fullmatch(name) for name in test_names], number=n
    )
    t_set = timeit.timeit(
        lambda: [is_snake_set_check(name) for name in test_names], number=n
    )
    t_builtin = timeit.timeit(
        lambda: [is_snake_builtin(name) for name in test_names], number=n
    )

    print(f"snake_case check (10 names, {n} iterations):")
    print(f"  regex match (original):  {t_match:.3f}s")
    print(f"  regex fullmatch:         {t_fullmatch:.3f}s")
    print(f"  frozenset check:         {t_set:.3f}s")
    print(f"  str.isidentifier:        {t_builtin:.3f}s")

    times = [t_match, t_fullmatch, t_set, t_builtin]
    names = ["regex_match", "regex_fullmatch", "set_check", "builtin"]
    fastest = names[times.index(min(times))]
    print(f"\nFastest: {fastest}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
