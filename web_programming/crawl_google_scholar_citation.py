"""
Crawl Google Scholar to retrieve citation counts for a paper.

Uses BeautifulSoup to parse the citation anchor from the scholar_lookup endpoint.
"""

import requests
from bs4 import BeautifulSoup

SCHOLAR_BASE_URL = "https://scholar.google.com/scholar_lookup"


def build_scholar_params(
    title: str,
    journal: str = "",
    volume: int = 0,
    pages: str = "",
    year: int = 0,
    hl: str = "en",
) -> dict:
    """
    Build query parameters dict for Google Scholar lookup.

    >>> p = build_scholar_params("Some Paper", journal="Nature", year=2020)
    >>> p["title"]
    'Some Paper'
    >>> p["journal"]
    'Nature'
    >>> p["year"]
    2020
    """
    return {
        "title": title,
        "journal": journal,
        "volume": volume,
        "pages": pages,
        "year": year,
        "hl": hl,
    }


def get_citation(base_url: str, params: dict) -> str:
    """
    Return the citation count string for a paper.

    >>> get_citation(SCHOLAR_BASE_URL, {})  # doctest: +SKIP
    'Cited by 42'
    """
    soup = BeautifulSoup(
        requests.get(base_url, params=params, timeout=10).content, "html.parser"
    )
    div = soup.find("div", attrs={"class": "gs_ri"})
    anchors = div.find("div", attrs={"class": "gs_fl"}).find_all("a")
    return anchors[2].get_text()


if __name__ == "__main__":
    params = build_scholar_params(
        title=(
            "Precisely geometry controlled microsupercapacitors for ultrahigh areal "
            "capacitance, volumetric capacitance, and energy density"
        ),
        journal="Chem. Mater.",
        volume=30,
        pages="3979-3990",
        year=2018,
    )
    print(get_citation(SCHOLAR_BASE_URL, params=params))
