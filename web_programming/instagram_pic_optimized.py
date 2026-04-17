"""
Instagram Pic – three og:image parsing approaches + benchmark.

Approach 1: BeautifulSoup find (original)
Approach 2: lxml XPath meta
Approach 3: regex on raw HTML
"""

import re
import time

SAMPLE_HTML = """
<html>
<head>
  <meta property="og:image" content="https://example.com/image.jpg" />
  <meta property="og:title" content="Test Post" />
</head>
<body></body>
</html>
"""


# ---------------------------------------------------------------------------
# Approach 1 – BeautifulSoup
# ---------------------------------------------------------------------------
def extract_og_image_bs4(html: str) -> str | None:
    """
    Extract og:image URL using BeautifulSoup.

    >>> extract_og_image_bs4(SAMPLE_HTML)
    'https://example.com/image.jpg'
    >>> extract_og_image_bs4("<html></html>") is None
    True
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("meta", {"property": "og:image"})
    if tag:
        return tag.get("content")
    return None


# ---------------------------------------------------------------------------
# Approach 2 – lxml XPath
# ---------------------------------------------------------------------------
def extract_og_image_lxml(html: str) -> str | None:
    """
    Extract og:image URL using lxml XPath.

    >>> extract_og_image_lxml(SAMPLE_HTML)
    'https://example.com/image.jpg'
    >>> extract_og_image_lxml("<html></html>") is None
    True
    """
    from lxml import html as lxml_html

    tree = lxml_html.fromstring(html.encode())
    results = tree.xpath('//meta[@property="og:image"]/@content')
    return results[0] if results else None


# ---------------------------------------------------------------------------
# Approach 3 – regex
# ---------------------------------------------------------------------------
_OG_IMAGE_RE = re.compile(
    r'<meta\s+property=["\']og:image["\']\s+content=["\'](https?://[^"\']+)["\']',
    re.IGNORECASE,
)


def extract_og_image_regex(html: str) -> str | None:
    """
    Extract og:image URL using regex (no parser dependency).

    >>> extract_og_image_regex(SAMPLE_HTML)
    'https://example.com/image.jpg'
    >>> extract_og_image_regex("<html></html>") is None
    True
    """
    m = _OG_IMAGE_RE.search(html)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 20_000) -> None:
    approaches = [
        ("BeautifulSoup", extract_og_image_bs4),
        ("lxml XPath", extract_og_image_lxml),
        ("regex", extract_og_image_regex),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(SAMPLE_HTML)
        elapsed = time.perf_counter() - t0
        print(f"{name:15s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.2f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
