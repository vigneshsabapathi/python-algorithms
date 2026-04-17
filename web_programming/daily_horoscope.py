"""
Fetch daily horoscope text from horoscope.com.

Zodiac signs are numbered 1 (Aries) through 12 (Pisces).
Day options: 'yesterday', 'today', 'tomorrow'.
"""

import requests
from bs4 import BeautifulSoup

HOROSCOPE_BASE_URL = (
    "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx"
)

ZODIAC_SIGNS = {
    1: "Aries",
    2: "Taurus",
    3: "Gemini",
    4: "Cancer",
    5: "Leo",
    6: "Virgo",
    7: "Libra",
    8: "Scorpio",
    9: "Sagittarius",
    10: "Capricorn",
    11: "Aquarius",
    12: "Pisces",
}


def build_horoscope_url(day: str, zodiac_sign: int) -> str:
    """
    Build the horoscope.com URL for a given day and zodiac sign number.

    >>> build_horoscope_url("today", 1)
    'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=1'
    >>> build_horoscope_url("tomorrow", 5)
    'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-tomorrow.aspx?sign=5'
    """
    return HOROSCOPE_BASE_URL.format(day=day) + f"?sign={zodiac_sign}"


def horoscope(zodiac_sign: int, day: str) -> str:
    """
    Fetch and return the horoscope text for a zodiac sign and day.

    >>> horoscope(1, "today")  # doctest: +SKIP
    'Today is a great day...'
    """
    url = build_horoscope_url(day, zodiac_sign)
    soup = BeautifulSoup(requests.get(url, timeout=10).content, "html.parser")
    return soup.find("div", class_="main-horoscope").p.text


if __name__ == "__main__":
    print("Daily Horoscope.\n")
    for num, sign in ZODIAC_SIGNS.items():
        print(f"{num}. {sign}")
    zodiac_sign = int(input("\nEnter your Zodiac sign number: ").strip())
    print("Choose a day: yesterday / today / tomorrow")
    day = input("Enter the day: ").strip()
    print(horoscope(zodiac_sign, day))
