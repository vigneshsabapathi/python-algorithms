"""
GitHub Info – three header-building approaches + benchmark.

Approach 1: plain dict (original)
Approach 2: dataclass-based header builder
Approach 3: dict union operator (Python 3.9+)
"""

import time
from dataclasses import dataclass

GITHUB_API_BASE = "https://api.github.com"


# ---------------------------------------------------------------------------
# Approach 1 – plain dict
# ---------------------------------------------------------------------------
def build_headers_dict(auth_token: str) -> dict:
    """
    Build GitHub API headers as a plain dict.

    >>> h = build_headers_dict("ghp_abc123")
    >>> h["Authorization"]
    'token ghp_abc123'
    >>> h["Accept"]
    'application/vnd.github.v3+json'
    """
    return {
        "Authorization": f"token {auth_token}",
        "Accept": "application/vnd.github.v3+json",
    }


# ---------------------------------------------------------------------------
# Approach 2 – dataclass helper
# ---------------------------------------------------------------------------
@dataclass
class GitHubHeaders:
    auth_token: str
    accept: str = "application/vnd.github.v3+json"

    def to_dict(self) -> dict:
        return {
            "Authorization": f"token {self.auth_token}",
            "Accept": self.accept,
        }


def build_headers_dataclass(auth_token: str) -> dict:
    """
    Build GitHub API headers via a dataclass.

    >>> h = build_headers_dataclass("ghp_abc123")
    >>> h["Authorization"]
    'token ghp_abc123'
    """
    return GitHubHeaders(auth_token=auth_token).to_dict()


# ---------------------------------------------------------------------------
# Approach 3 – base headers + union merge (Python 3.9+)
# ---------------------------------------------------------------------------
_BASE_HEADERS = {"Accept": "application/vnd.github.v3+json"}


def build_headers_union(auth_token: str) -> dict:
    """
    Build GitHub API headers using dict union (Python 3.9+).

    >>> h = build_headers_union("ghp_abc123")
    >>> h["Authorization"]
    'token ghp_abc123'
    >>> h["Accept"]
    'application/vnd.github.v3+json'
    """
    return _BASE_HEADERS | {"Authorization": f"token {auth_token}"}


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    token = "ghp_test_token_abc123"
    approaches = [
        ("plain dict", build_headers_dict),
        ("dataclass", build_headers_dataclass),
        ("dict union", build_headers_union),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(token)
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
