"""
Download Images – three regex extraction approaches + benchmark.

Approach 1: re.findall with complex pattern (original)
Approach 2: re.finditer (lazy, stops early)
Approach 3: compiled pattern reuse
"""

import re
import time

THUMBNAIL_PATTERN = (
    r"\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]"
)
FULL_RES_PATTERN = r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]"

_THUMBNAIL_RE = re.compile(THUMBNAIL_PATTERN)
_FULL_RES_RE = re.compile(FULL_RES_PATTERN)

SAMPLE_DATA = (
    '["https://encrypted-tbn0.gstatic.com/images?q=abc",80,60],'
    ',["https://www.example.com/image1.jpg",800,600],'
    ',["https://www.example.com/image2.jpg",1024,768]'
)


# ---------------------------------------------------------------------------
# Approach 1 – re.findall (original flow, recompiles)
# ---------------------------------------------------------------------------
def extract_images_findall(data: str) -> list[str]:
    """
    Extract full-resolution image URLs using re.findall.

    >>> urls = extract_images_findall(SAMPLE_DATA)
    >>> len(urls)
    2
    >>> urls[0]
    'https://www.example.com/image1.jpg'
    """
    removed = re.sub(THUMBNAIL_PATTERN, "", data)
    return re.findall(FULL_RES_PATTERN, removed)


# ---------------------------------------------------------------------------
# Approach 2 – re.finditer (lazy iteration)
# ---------------------------------------------------------------------------
def extract_images_finditer(data: str, max_images: int = 50) -> list[str]:
    """
    Extract full-resolution image URLs using re.finditer (stops at max).

    >>> urls = extract_images_finditer(SAMPLE_DATA)
    >>> len(urls)
    2
    """
    removed = _THUMBNAIL_RE.sub("", data)
    return [
        m.group(1)
        for i, m in enumerate(_FULL_RES_RE.finditer(removed))
        if i < max_images
    ]


# ---------------------------------------------------------------------------
# Approach 3 – pre-compiled patterns
# ---------------------------------------------------------------------------
def extract_images_compiled(data: str) -> list[str]:
    """
    Extract full-resolution image URLs using pre-compiled regex patterns.

    >>> urls = extract_images_compiled(SAMPLE_DATA)
    >>> len(urls)
    2
    >>> urls[1]
    'https://www.example.com/image2.jpg'
    """
    removed = _THUMBNAIL_RE.sub("", data)
    return _FULL_RES_RE.findall(removed)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 50_000) -> None:
    approaches = [
        ("findall (recompile)", extract_images_findall),
        ("finditer", extract_images_finditer),
        ("compiled", extract_images_compiled),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(SAMPLE_DATA)
        elapsed = time.perf_counter() - t0
        print(f"{name:22s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.2f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
