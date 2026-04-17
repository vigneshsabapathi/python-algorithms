"""
World COVID-19 Stats – three HTML parsing approaches + benchmark.

Approach 1: BeautifulSoup (original)
Approach 2: lxml XPath
Approach 3: regex extraction
"""

import re
import time

SAMPLE_HTML = """
<html><body>
  <h1>Coronavirus Cases:</h1>
  <div class="maincounter-number"><span>615,413,902 </span></div>
  <h1>Deaths:</h1>
  <div class="maincounter-number"><span>6,537,706 </span></div>
  <h1>Recovered:</h1>
  <div class="maincounter-number"><span>595,854,006 </span></div>
  <span class="panel-title">Active Cases</span>
  <div class="number-table-main">12,000,000</div>
</body></html>
"""


# ---------------------------------------------------------------------------
# Approach 1 – BeautifulSoup (original)
# ---------------------------------------------------------------------------
def parse_stats_bs4(html: str) -> dict:
    """
    Parse COVID stats using BeautifulSoup.

    >>> stats = parse_stats_bs4(SAMPLE_HTML)
    >>> stats["Coronavirus Cases:"]
    '615,413,902'
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    keys = soup.find_all("h1")
    values = soup.find_all("div", {"class": "maincounter-number"})
    keys += soup.find_all("span", {"class": "panel-title"})
    values += soup.find_all("div", {"class": "number-table-main"})
    return {k.text.strip(): v.text.strip() for k, v in zip(keys, values)}


# ---------------------------------------------------------------------------
# Approach 2 – lxml XPath
# ---------------------------------------------------------------------------
def parse_stats_lxml(html: str) -> dict:
    """
    Parse COVID stats using lxml XPath.

    >>> stats = parse_stats_lxml(SAMPLE_HTML)
    >>> "615,413,902" in list(stats.values())[0]
    True
    """
    from lxml import html as lxml_html

    tree = lxml_html.fromstring(html.encode())
    keys = [el.text_content().strip() for el in tree.xpath("//h1")]
    values = [
        el.text_content().strip()
        for el in tree.xpath('//div[@class="maincounter-number"]')
    ]
    keys += [el.text_content().strip() for el in tree.xpath('//span[@class="panel-title"]')]
    values += [
        el.text_content().strip()
        for el in tree.xpath('//div[@class="number-table-main"]')
    ]
    return dict(zip(keys, values))


# ---------------------------------------------------------------------------
# Approach 3 – regex
# ---------------------------------------------------------------------------
_H1_RE = re.compile(r"<h1>([^<]+)</h1>")
_COUNTER_RE = re.compile(r'class="maincounter-number"><span>([^<]+)</span>')


def parse_stats_regex(html: str) -> dict:
    """
    Parse COVID main counters using regex (no parser).

    >>> stats = parse_stats_regex(SAMPLE_HTML)
    >>> len(stats)
    3
    """
    keys = [m.group(1).strip() for m in _H1_RE.finditer(html)]
    values = [m.group(1).strip() for m in _COUNTER_RE.finditer(html)]
    return dict(zip(keys, values))


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 5000) -> None:
    approaches = [
        ("BeautifulSoup", parse_stats_bs4),
        ("lxml XPath", parse_stats_lxml),
        ("regex", parse_stats_regex),
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
