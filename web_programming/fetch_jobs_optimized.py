"""
Fetch Jobs – three job-data extraction approaches + benchmark.

Approach 1: BeautifulSoup .find() (original)
Approach 2: lxml XPath
Approach 3: regex on raw HTML
"""

import re
import time

SAMPLE_HTML = """
<div data-tn-component="organicJob">
  <a data-tn-element="jobTitle">Senior Python Developer</a>
  <span class="company">TechCorp Ltd</span>
</div>
<div data-tn-component="organicJob">
  <a data-tn-element="jobTitle">Backend Engineer</a>
  <span class="company">StartupXYZ</span>
</div>
"""

INDEED_BASE_URL = "https://www.indeed.co.in/jobs?q=mobile+app+development&l="


def build_indeed_url(location: str) -> str:
    """
    Build the Indeed job search URL for a given location.

    >>> build_indeed_url("mumbai")
    'https://www.indeed.co.in/jobs?q=mobile+app+development&l=mumbai'
    >>> build_indeed_url("Bangalore")
    'https://www.indeed.co.in/jobs?q=mobile+app+development&l=Bangalore'
    """
    return INDEED_BASE_URL + location


# ---------------------------------------------------------------------------
# Approach 1 – BeautifulSoup (original)
# ---------------------------------------------------------------------------
def extract_jobs_bs4(html: str) -> list[tuple[str, str]]:
    """
    Extract (job_title, company) pairs using BeautifulSoup.

    >>> jobs = extract_jobs_bs4(SAMPLE_HTML)
    >>> jobs[0]
    ('Senior Python Developer', 'TechCorp Ltd')
    >>> jobs[1]
    ('Backend Engineer', 'StartupXYZ')
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    result = []
    for job in soup.find_all("div", attrs={"data-tn-component": "organicJob"}):
        title_tag = job.find("a", attrs={"data-tn-element": "jobTitle"})
        company_tag = job.find("span", {"class": "company"})
        if title_tag and company_tag:
            result.append((title_tag.text.strip(), company_tag.text.strip()))
    return result


# ---------------------------------------------------------------------------
# Approach 2 – lxml XPath
# ---------------------------------------------------------------------------
def extract_jobs_lxml(html: str) -> list[tuple[str, str]]:
    """
    Extract (job_title, company) pairs using lxml XPath.

    >>> jobs = extract_jobs_lxml(SAMPLE_HTML)
    >>> jobs[0]
    ('Senior Python Developer', 'TechCorp Ltd')
    """
    from lxml import html as lxml_html

    tree = lxml_html.fromstring(html)
    jobs_divs = tree.xpath('//div[@data-tn-component="organicJob"]')
    result = []
    for div in jobs_divs:
        titles = div.xpath('.//a[@data-tn-element="jobTitle"]/text()')
        companies = div.xpath('.//span[@class="company"]/text()')
        if titles and companies:
            result.append((titles[0].strip(), companies[0].strip()))
    return result


# ---------------------------------------------------------------------------
# Approach 3 – regex
# ---------------------------------------------------------------------------
_JOB_RE = re.compile(
    r'data-tn-element="jobTitle"[^>]*>([^<]+)</a>.*?class="company"[^>]*>([^<]+)</span>',
    re.DOTALL,
)


def extract_jobs_regex(html: str) -> list[tuple[str, str]]:
    """
    Extract (job_title, company) pairs using regex.

    >>> jobs = extract_jobs_regex(SAMPLE_HTML)
    >>> jobs[0]
    ('Senior Python Developer', 'TechCorp Ltd')
    """
    return [(t.strip(), c.strip()) for t, c in _JOB_RE.findall(html)]


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 5000) -> None:
    approaches = [
        ("BeautifulSoup", extract_jobs_bs4),
        ("lxml XPath", extract_jobs_lxml),
        ("regex", extract_jobs_regex),
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
