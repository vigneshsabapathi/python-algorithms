"""
Google Scholar Citation – three params-building approaches + benchmark.

Approach 1: plain dict literal
Approach 2: dataclass-based params
Approach 3: TypedDict-based params
"""

import time
from dataclasses import asdict, dataclass
from typing import TypedDict


# ---------------------------------------------------------------------------
# Approach 1 – plain dict
# ---------------------------------------------------------------------------
def build_params_dict(title: str, journal: str, volume: int, pages: str, year: int) -> dict:
    """
    Build scholar lookup params as a plain dict.

    >>> p = build_params_dict("Paper A", "Nature", 10, "1-10", 2021)
    >>> p["title"]
    'Paper A'
    >>> p["year"]
    2021
    """
    return {
        "title": title,
        "journal": journal,
        "volume": volume,
        "pages": pages,
        "year": year,
        "hl": "en",
    }


# ---------------------------------------------------------------------------
# Approach 2 – dataclass
# ---------------------------------------------------------------------------
@dataclass
class ScholarParams:
    title: str
    journal: str
    volume: int
    pages: str
    year: int
    hl: str = "en"

    def to_dict(self) -> dict:
        return asdict(self)


def build_params_dataclass(title: str, journal: str, volume: int, pages: str, year: int) -> dict:
    """
    Build scholar lookup params via a dataclass.

    >>> p = build_params_dataclass("Paper A", "Nature", 10, "1-10", 2021)
    >>> p["title"]
    'Paper A'
    >>> p["hl"]
    'en'
    """
    return ScholarParams(title=title, journal=journal, volume=volume, pages=pages, year=year).to_dict()


# ---------------------------------------------------------------------------
# Approach 3 – TypedDict
# ---------------------------------------------------------------------------
class ScholarTypedDict(TypedDict):
    title: str
    journal: str
    volume: int
    pages: str
    year: int
    hl: str


def build_params_typeddict(title: str, journal: str, volume: int, pages: str, year: int) -> ScholarTypedDict:
    """
    Build scholar lookup params as a TypedDict (same dict, type-safe at static check).

    >>> p = build_params_typeddict("Paper B", "Science", 5, "100-110", 2020)
    >>> p["journal"]
    'Science'
    """
    return ScholarTypedDict(title=title, journal=journal, volume=volume, pages=pages, year=year, hl="en")


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 300_000) -> None:
    args = ("Precision Test", "Chem. Mater.", 30, "3979-3990", 2018)
    approaches = [
        ("plain dict", build_params_dict),
        ("dataclass", build_params_dataclass),
        ("TypedDict", build_params_typeddict),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(*args)
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
