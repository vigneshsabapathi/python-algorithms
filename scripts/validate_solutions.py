"""
Validate that all Python solution files in the repository pass their doctests.

Walks the project tree, discovers .py files, runs their doctests, and reports
pass/fail status. Used as a CI check to ensure all algorithms have working examples.

Source: https://github.com/TheAlgorithms/Python/blob/master/scripts/validate_solutions.py
"""

from __future__ import annotations

import doctest
import importlib.util
import os
import sys
from pathlib import Path


def has_doctests(filepath: str) -> bool:
    """
    Check if a Python file contains doctest examples (lines with '>>>').

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w")
    >>> _ = tmp.write('def f():\\n    \"\"\"\\n    >>> f()\\n    1\\n    \"\"\"\\n    return 1\\n')
    >>> tmp.close()
    >>> has_doctests(tmp.name)
    True
    >>> os.unlink(tmp.name)

    >>> tmp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w")
    >>> _ = tmp2.write("def f():\\n    return 1\\n")
    >>> tmp2.close()
    >>> has_doctests(tmp2.name)
    False
    >>> os.unlink(tmp2.name)
    """
    content = Path(filepath).read_text(encoding="utf-8", errors="replace")
    return ">>>" in content


def count_doctests(filepath: str) -> int:
    """
    Count the number of doctest examples in a Python file.

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w")
    >>> _ = tmp.write('def f():\\n    \"\"\"\\n    >>> f()\\n    1\\n    >>> f() + 1\\n    2\\n    \"\"\"\\n    return 1\\n')
    >>> tmp.close()
    >>> count_doctests(tmp.name)
    2
    >>> os.unlink(tmp.name)
    """
    content = Path(filepath).read_text(encoding="utf-8", errors="replace")
    return sum(1 for line in content.splitlines() if line.strip().startswith(">>>"))


def should_validate(filepath: Path, root: Path) -> bool:
    """
    Determine if a file should have its doctests validated.

    Skips hidden dirs, __pycache__, venv, __init__.py, and files without doctests.

    >>> should_validate(Path("sorts/bubble_sort.py"), Path("."))
    True
    >>> should_validate(Path(".git/hooks/pre-commit"), Path("."))
    False
    >>> should_validate(Path("sorts/__init__.py"), Path("."))
    False
    >>> should_validate(Path("venv/lib/site.py"), Path("."))
    False
    """
    rel = filepath.relative_to(root) if root != Path(".") else filepath
    parts = rel.parts
    excluded = {".git", "__pycache__", "venv", ".venv", "node_modules"}
    for part in parts:
        if part.startswith(".") and part != ".":
            return False
        if part in excluded:
            return False
    if filepath.name == "__init__.py":
        return False
    if not filepath.suffix == ".py":
        return False
    return True


def run_doctest_on_file(filepath: str) -> dict:
    """
    Run doctests on a single Python file.

    Returns dict with keys: filepath, attempted, failed, passed, error.

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w")
    >>> _ = tmp.write('def add(a, b):\\n    \"\"\"\\n    >>> add(1, 2)\\n    3\\n    \"\"\"\\n    return a + b\\n')
    >>> tmp.close()
    >>> result = run_doctest_on_file(tmp.name)
    >>> result["passed"]
    True
    >>> result["attempted"]
    1
    >>> result["failed"]
    0
    >>> os.unlink(tmp.name)
    """
    try:
        spec = importlib.util.spec_from_file_location("_test_module", filepath)
        if spec is None or spec.loader is None:
            return {
                "filepath": filepath,
                "attempted": 0,
                "failed": 0,
                "passed": False,
                "error": "Could not load module spec",
            }
        module = importlib.util.module_from_spec(spec)
        # Temporarily add parent dir to sys.path for imports
        parent_dir = str(Path(filepath).parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            return {
                "filepath": filepath,
                "attempted": 0,
                "failed": 0,
                "passed": False,
                "error": f"Import error: {e}",
            }
        results = doctest.testmod(module, verbose=False)
        return {
            "filepath": filepath,
            "attempted": results.attempted,
            "failed": results.failed,
            "passed": results.failed == 0,
            "error": None,
        }
    except Exception as e:
        return {
            "filepath": filepath,
            "attempted": 0,
            "failed": 0,
            "passed": False,
            "error": str(e),
        }


def validate_all(root: Path) -> dict:
    """
    Validate all Python files in the repository.

    Returns summary dict with: total, passed, failed, errors, details.
    """
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in sorted(dirnames)
            if not d.startswith(".") and d not in {"__pycache__", "venv", ".venv"}
        ]
        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            if not should_validate(fpath, root):
                continue
            if not has_doctests(str(fpath)):
                continue
            result = run_doctest_on_file(str(fpath))
            results.append(result)

    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"] and r["error"] is None)
    errors = sum(1 for r in results if r["error"] is not None)

    return {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "details": results,
    }


if __name__ == "__main__":
    import doctest as dt

    dt.testmod(verbose=True)

    print("\n--- validate_solutions demo ---")
    root = Path(__file__).resolve().parent.parent
    summary = validate_all(root)
    print(f"Total files with doctests: {summary['total']}")
    print(f"  Passed: {summary['passed']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Errors: {summary['errors']}")
    if summary["failed"] > 0 or summary["errors"] > 0:
        print("\nFailing files:")
        for r in summary["details"]:
            if not r["passed"]:
                err = f" ({r['error']})" if r["error"] else ""
                print(f"  {r['filepath']}: {r['failed']} failed{err}")
