"""
Get CO2 emission data from the UK CarbonIntensity API.

API docs: https://api.carbonintensity.org.uk/
"""

from datetime import date

import requests

BASE_URL = "https://api.carbonintensity.org.uk/intensity"


def fetch_last_half_hour() -> str:
    """
    Return the actual CO2 intensity for the last half hour.

    >>> isinstance(fetch_last_half_hour(), (str, int, float, type(None)))  # doctest: +SKIP
    True
    """
    last_half_hour = requests.get(BASE_URL, timeout=10).json()["data"][0]
    return last_half_hour["intensity"]["actual"]


def fetch_from_to(start: date, end: date) -> list:
    """
    Return CO2 emission data for a date range.

    >>> isinstance(fetch_from_to(date(2020,10,1), date(2020,10,3)), list)  # doctest: +SKIP
    True
    """
    return requests.get(f"{BASE_URL}/{start}/{end}", timeout=10).json()["data"]


if __name__ == "__main__":
    for entry in fetch_from_to(start=date(2020, 10, 1), end=date(2020, 10, 3)):
        print("from {from} to {to}: {intensity[actual]}".format(**entry))
    print(f"{fetch_last_half_hour() = }")
