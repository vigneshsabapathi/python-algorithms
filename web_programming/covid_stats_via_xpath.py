"""
Fetch simple COVID-19 statistics from the Worldometers archive site using lxml.

lxml is chosen over BeautifulSoup for its speed and XPath support.
"""

from typing import NamedTuple

import requests
from lxml import html


class CovidData(NamedTuple):
    cases: str
    deaths: str
    recovered: str


def covid_stats(
    url: str = (
        "https://web.archive.org/web/20250825095350/"
        "https://www.worldometers.info/coronavirus/"
    ),
) -> CovidData:
    """
    Fetch COVID-19 worldwide statistics via XPath.

    >>> covid_stats()  # doctest: +SKIP
    CovidData(cases=..., deaths=..., recovered=...)
    """
    xpath_str = '//div[@class = "maincounter-number"]/span/text()'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        print("Request timed out.")
        return CovidData("N/A", "N/A", "N/A")
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return CovidData("N/A", "N/A", "N/A")
    data = html.fromstring(response.content).xpath(xpath_str)
    if len(data) != 3:
        print("Unexpected data format. The page structure may have changed.")
        data = "N/A", "N/A", "N/A"
    return CovidData(*data)


if __name__ == "__main__":
    fmt = (
        "Total COVID-19 cases in the world: {}\n"
        "Total deaths due to COVID-19 in the world: {}\n"
        "Total COVID-19 patients recovered in the world: {}"
    )
    print(fmt.format(*covid_stats()))
