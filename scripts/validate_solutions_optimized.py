"""
Optimized solution validator with multiple doctest-discovery strategies.

Improvements over the original:
- AST-based discovery: Parses the file's AST to find functions with docstrings
  containing '>>>' — avoids importing modules that have side effects.
- Subprocess isolation: Runs each file's doctests in a subprocess, preventing
  import pollution and catching segfaults/hangs with timeouts.
- Parallel validation: Uses concurrent.futures to validate multiple files
  simultaneously, reducing wall-clock time on multi-core machines.
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


# --- Doctest discovery strategies ---

def has_doctests_grep(filepath: str) -> bool:
    """
    Original: simple string search for '>>>'.

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w")
    >>> _ = tmp.write('def f():\\n    \"\"\"\\n    >>> 1+1\\n    2\\n    \"\"\"\\n    pass\\n')
    >>> tmp.close()
    >>> has_doctests_grep(tmp.name)
    True
    >>> os.unlink(tmp.name)
    """
    return ">>>" in Path(filepath).read_text(encoding="utf-8", errors="replace")


def has_doctests_ast(filepath: str) -> bool:
    """
    AST-based: parse file, check docstrings for '>>>'.
    More precise — ignores '>>>' in comments or string literals outside docstrings.

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w")
    >>> _ = tmp.write('def f():\\n    \"\"\"\\n    >>> 1+1\\n    2\\n    \"\"\"\\n    pass\\n')
    >>> tmp.close()
    >>> has_doctests_ast(tmp.name)
    True
    >>> os.unlink(tmp.name)

    >>> tmp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w")
    >>> _ = tmp2.write('# >>> this is a comment, not a doctest\\ndef f(): pass\\n')
    >>> tmp2.close()
    >>> has_doctests_ast(tmp2.name)
    False
    >>> os.unlink(tmp2.name)
    """
    try:
        source = Path(filepath).read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except SyntaxError:
        return False

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node)
            if docstring and ">>>" in docstring:
                return True
    return False


def count_doctest_examples_ast(filepath: str) -> int:
    """
    Count doctest examples using AST — only counts '>>>' in actual docstrings.

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w")
    >>> _ = tmp.write('def f():\\n    \"\"\"\\n    >>> 1\\n    1\\n    >>> 2\\n    2\\n    \"\"\"\\n    pass\\n')
    >>> tmp.close()
    >>> count_doctest_examples_ast(tmp.name)
    2
    >>> os.unlink(tmp.name)
    """
    try:
        source = Path(filepath).read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except SyntaxError:
        return 0

    count = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node)
            if docstring:
                count += sum(1 for line in docstring.splitlines() if line.strip().startswith(">>>"))
    return count


# --- Validation strategies ---

def validate_by_import(filepath: str) -> dict:
    """
    Original: import module and run doctest.testmod().
    """
    import doctest
    import importlib.util

    try:
        spec = importlib.util.spec_from_file_location("_mod", filepath)
        if spec is None or spec.loader is None:
            return {"filepath": filepath, "passed": False, "error": "No spec"}
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        results = doctest.testmod(module, verbose=False)
        return {
            "filepath": filepath,
            "attempted": results.attempted,
            "failed": results.failed,
            "passed": results.failed == 0,
            "error": None,
        }
    except Exception as e:
        return {"filepath": filepath, "attempted": 0, "failed": 0, "passed": False, "error": str(e)}


def validate_by_subprocess(filepath: str, timeout: int = 30) -> dict:
    """
    Run doctests in an isolated subprocess — prevents import side effects.
    """
    cmd = [sys.executable, "-m", "doctest", "-v", filepath]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        # doctest returns 0 on success, 1 on failure
        passed = result.returncode == 0
        # Count attempted/failed from output
        attempted = result.stdout.count("Trying:")
        # "***" lines indicate failures
        failed = result.stdout.count("Failed examples")
        return {
            "filepath": filepath,
            "attempted": attempted,
            "failed": 0 if passed else max(1, failed),
            "passed": passed,
            "error": None,
        }
    except subprocess.TimeoutExpired:
        return {"filepath": filepath, "attempted": 0, "failed": 0, "passed": False, "error": f"Timeout ({timeout}s)"}
    except Exception as e:
        return {"filepath": filepath, "attempted": 0, "failed": 0, "passed": False, "error": str(e)}


def validate_all_parallel(root: Path, max_workers: int = 4) -> dict:
    """
    Validate all files in parallel using subprocess isolation.
    """
    skip_dirs = {".git", "__pycache__", "venv", ".venv", "node_modules"}
    files_to_check = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in sorted(dirnames) if d not in skip_dirs and not d.startswith(".")]
        for fname in sorted(filenames):
            if not fname.endswith(".py") or fname == "__init__.py":
                continue
            fpath = str(Path(dirpath) / fname)
            if has_doctests_grep(fpath):
                files_to_check.append(fpath)

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(validate_by_subprocess, fp): fp
            for fp in files_to_check
        }
        for future in as_completed(futures):
            results.append(future.result())

    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"] and r.get("error") is None)
    errors = sum(1 for r in results if r.get("error") is not None)

    return {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "details": sorted(results, key=lambda r: r["filepath"]),
    }


def benchmark() -> None:
    """Benchmark doctest discovery strategies."""
    import tempfile
    import timeit

    # Create test files
    with_doctest = tempfile.NamedTemporaryFile(
        delete=False, suffix=".py", mode="w"
    )
    with_doctest.write(
        'def f():\n    """\n    >>> f()\n    1\n    """\n    return 1\n'
    )
    with_doctest.close()

    without_doctest = tempfile.NamedTemporaryFile(
        delete=False, suffix=".py", mode="w"
    )
    without_doctest.write("def f():\n    return 1\n")
    without_doctest.close()

    files = [with_doctest.name, without_doctest.name]
    n = 50_000

    t_grep = timeit.timeit(
        lambda: [has_doctests_grep(f) for f in files], number=n
    )
    t_ast = timeit.timeit(
        lambda: [has_doctests_ast(f) for f in files], number=n
    )

    print(f"Doctest discovery ({n} iterations, 2 files):")
    print(f"  grep ('>>>' search):  {t_grep:.3f}s")
    print(f"  AST (parse + walk):   {t_ast:.3f}s")

    fastest = "grep" if t_grep < t_ast else "AST"
    ratio = max(t_grep, t_ast) / min(t_grep, t_ast)
    print(f"\nFastest: {fastest} ({ratio:.1f}x faster)")

    os.unlink(with_doctest.name)
    os.unlink(without_doctest.name)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
