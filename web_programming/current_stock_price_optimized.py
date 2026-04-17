"""
Current Stock Price – three HTML parsing approaches + benchmark.

Approach 1: BeautifulSoup find (original)
Approach 2: lxml CSS select
Approach 3: regex on raw HTML
"""

import re
import time

SAMPLE_HTML = """
<html><body>
  <span data-testid="qsp-price" class="livePrice">228.43</span>
</body></html>
"""


# ---------------------------------------------------------------------------
# Approach 1 – BeautifulSoup find
# ---------------------------------------------------------------------------
def parse_price_bs4(html: str) -> str:
    """
    Extract stock price using BeautifulSoup .find().

    >>> parse_price_bs4(SAMPLE_HTML)
    '228.43'
    >>> parse_price_bs4("<html></html>")
    'Not found.'
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("span", {"data-testid": "qsp-price"})
    return tag.get_text() if tag else "Not found."


# ---------------------------------------------------------------------------
# Approach 2 – lxml CSS select
# ---------------------------------------------------------------------------
def parse_price_lxml(html: str) -> str:
    """
    Extract stock price using lxml cssselect.

    >>> parse_price_lxml(SAMPLE_HTML)
    '228.43'
    >>> parse_price_lxml("<html></html>")
    'Not found.'
    """
    from lxml import html as lxml_html

    tree = lxml_html.fromstring(html)
    results = tree.cssselect('span[data-testid="qsp-price"]')
    return results[0].text_content() if results else "Not found."


# ---------------------------------------------------------------------------
# Approach 3 – regex
# ---------------------------------------------------------------------------
_PRICE_RE = re.compile(r'data-testid="qsp-price"[^>]*>([^<]+)<')


def parse_price_regex(html: str) -> str:
    """
    Extract stock price using a regex pattern.

    >>> parse_price_regex(SAMPLE_HTML)
    '228.43'
    >>> parse_price_regex("<html></html>")
    'Not found.'
    """
    m = _PRICE_RE.search(html)
    return m.group(1) if m else "Not found."


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 10_000) -> None:
    approaches = [
        ("BeautifulSoup", parse_price_bs4),
        ("lxml", parse_price_lxml),
        ("regex", parse_price_regex),
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
