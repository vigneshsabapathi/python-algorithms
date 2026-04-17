"""
Random Anime Character – three image-filename-generation approaches + benchmark.

Approach 1: os.path.splitext + replace + strip (original)
Approach 2: pathlib.Path
Approach 3: regex extraction
"""

import os
import re
import time
from pathlib import Path

SAMPLE_IMAGE_URL = "https://cdn.mywaifulist.moe/characters/Nezuko_Kamado.png"
SAMPLE_TITLE = "  Nezuko Kamado  "


# ---------------------------------------------------------------------------
# Approach 1 – os.path.splitext (original)
# ---------------------------------------------------------------------------
def build_filename_os(title: str, image_url: str) -> str:
    """
    Build image filename using os.path.splitext and str.replace.

    >>> build_filename_os("  Nezuko Kamado  ", "https://cdn.example.com/img/Nezuko.png")
    'Nezuko_Kamado.png'
    """
    _, ext = os.path.splitext(os.path.basename(image_url))
    return title.strip().replace(" ", "_") + ext


# ---------------------------------------------------------------------------
# Approach 2 – pathlib.Path
# ---------------------------------------------------------------------------
def build_filename_pathlib(title: str, image_url: str) -> str:
    """
    Build image filename using pathlib.Path for extension extraction.

    >>> build_filename_pathlib("  Nezuko Kamado  ", "https://cdn.example.com/img/Nezuko.png")
    'Nezuko_Kamado.png'
    """
    ext = Path(image_url.split("?")[0]).suffix
    return title.strip().replace(" ", "_") + ext


# ---------------------------------------------------------------------------
# Approach 3 – regex
# ---------------------------------------------------------------------------
_EXT_RE = re.compile(r"(\.[a-zA-Z0-9]+)(?:\?|$)")


def build_filename_regex(title: str, image_url: str) -> str:
    """
    Build image filename using regex to extract the extension.

    >>> build_filename_regex("  Nezuko Kamado  ", "https://cdn.example.com/img/Nezuko.png")
    'Nezuko_Kamado.png'
    >>> build_filename_regex("Hero", "https://cdn.example.com/img/hero.jpg?v=1")
    'Hero.jpg'
    """
    m = _EXT_RE.search(image_url)
    ext = m.group(1) if m else ""
    return title.strip().replace(" ", "_") + ext


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 300_000) -> None:
    approaches = [
        ("os.path", build_filename_os),
        ("pathlib", build_filename_pathlib),
        ("regex", build_filename_regex),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(SAMPLE_TITLE, SAMPLE_IMAGE_URL)
        elapsed = time.perf_counter() - t0
        print(f"{name:10s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
