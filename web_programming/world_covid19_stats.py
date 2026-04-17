"""
Scrape and display current worldwide COVID-19 statistics from Worldometers.

Data source: https://www.worldometers.info/coronavirus/
"""

import requests
from bs4 import BeautifulSoup

WORLDOMETERS_URL = "https://www.worldometers.info/coronavirus/"


def world_covid19_stats(url: str = WORLDOMETERS_URL) -> dict:
    """
    Return a dict of worldwide COVID-19 statistics scraped from Worldometers.

    Keys are stat labels, values are numeric strings.

    >>> isinstance(world_covid19_stats(), dict)  # doctest: +SKIP
    True
    """
    soup = BeautifulSoup(
        requests.get(url, timeout=10).text, "html.parser"
    )
    keys = soup.find_all("h1")
    values = soup.find_all("div", {"class": "maincounter-number"})
    keys += soup.find_all("span", {"class": "panel-title"})
    values += soup.find_all("div", {"class": "number-table-main"})
    return {key.text.strip(): value.text.strip() for key, value in zip(keys, values)}


if __name__ == "__main__":
    print("\033[1m COVID-19 Status of the World \033[0m\n")
    print(
        "\n".join(
            f"{key}\n{value}" for key, value in world_covid19_stats().items()
        )
    )
