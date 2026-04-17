"""
COVID Stats via XPath – three parsing approaches + benchmark.

Approach 1: lxml XPath (fast, low-level)
Approach 2: BeautifulSoup with html.parser (pure Python, no C deps)
Approach 3: regex extraction (no parser, fastest on clean HTML)
"""

import re
import time
from typing import NamedTuple


class CovidData(NamedTuple):
    cases: str
    deaths: str
    recovered: str


SAMPLE_HTML = """
<html><body>
  <div class="maincounter-number"><span>615,413,902</span></div>
  <div class="maincounter-number"><span>6,537,706</span></div>
  <div class="maincounter-number"><span>595,854,006</span></div>
</body></html>
"""


# ---------------------------------------------------------------------------
# Approach 1 – lxml XPath
# ---------------------------------------------------------------------------
def parse_with_lxml(html: str) -> CovidData:
    """
    Parse COVID counters from HTML using lxml XPath.

    >>> parse_with_lxml(SAMPLE_HTML)
    CovidData(cases='615,413,902', deaths='6,537,706', recovered='595,854,006')
    """
    from lxml import html as lxml_html

    xpath_str = '//div[@class = "maincounter-number"]/span/text()'
    data = lxml_html.fromstring(html.encode()).xpath(xpath_str)
    return CovidData(*data) if len(data) == 3 else CovidData("N/A", "N/A", "N/A")


# ---------------------------------------------------------------------------
# Approach 2 – BeautifulSoup
# ---------------------------------------------------------------------------
def parse_with_bs4(html: str) -> CovidData:
    """
    Parse COVID counters from HTML using BeautifulSoup.

    >>> parse_with_bs4(SAMPLE_HTML)
    CovidData(cases='615,413,902', deaths='6,537,706', recovered='595,854,006')
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    spans = [
        div.find("span").text
        for div in soup.find_all("div", class_="maincounter-number")
        if div.find("span")
    ]
    return CovidData(*spans) if len(spans) == 3 else CovidData("N/A", "N/A", "N/A")


# ---------------------------------------------------------------------------
# Approach 3 – regex
# ---------------------------------------------------------------------------
def parse_with_regex(html: str) -> CovidData:
    """
    Parse COVID counters from HTML using regex (no parser dependency).

    >>> parse_with_regex(SAMPLE_HTML)
    CovidData(cases='615,413,902', deaths='6,537,706', recovered='595,854,006')
    """
    pattern = r'class="maincounter-number">\s*<span>([^<]+)</span>'
    matches = re.findall(pattern, html)
    return CovidData(*matches) if len(matches) == 3 else CovidData("N/A", "N/A", "N/A")


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 5000) -> None:
    approaches = [
        ("lxml XPath", parse_with_lxml),
        ("BeautifulSoup", parse_with_bs4),
        ("regex", parse_with_regex),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(SAMPLE_HTML)
        elapsed = time.perf_counter() - t0
        print(f"{name:20s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.2f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
