"""
Fetch NASA Astronomy Picture of the Day (APOD) and archive search data.

Get your free API key at https://api.nasa.gov/
"""

import requests

NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
NASA_IMAGES_URL = "https://images-api.nasa.gov/search"


def get_apod_data(api_key: str) -> dict:
    """
    Return the APOD (Astronomy Picture of the Day) metadata dict.

    Keys include: date, title, explanation, url, media_type, hdurl.

    >>> isinstance(get_apod_data("DEMO_KEY"), dict)  # doctest: +SKIP
    True
    """
    return requests.get(NASA_APOD_URL, params={"api_key": api_key}, timeout=10).json()


def save_apod(api_key: str, path: str = ".") -> dict:
    """
    Download the APOD image and save it locally; return the APOD metadata.

    >>> save_apod("DEMO_KEY")  # doctest: +SKIP
    {'date': '2024-01-01', 'title': '...', ...}
    """
    apod_data = get_apod_data(api_key)
    img_url = apod_data["url"]
    img_name = img_url.split("/")[-1]
    response = requests.get(img_url, timeout=30)
    with open(f"{path}/{img_name}", "wb+") as img_file:
        img_file.write(response.content)
    return apod_data


def get_archive_data(query: str) -> dict:
    """
    Search the NASA images archive for a query string.

    Returns a dict with a 'collection' key containing 'items'.

    >>> isinstance(get_archive_data("apollo 2011"), dict)  # doctest: +SKIP
    True
    """
    return requests.get(
        NASA_IMAGES_URL, params={"q": query}, timeout=10
    ).json()


if __name__ == "__main__":
    import os

    api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
    print(save_apod(api_key))
    apollo_items = get_archive_data("apollo 2011")["collection"]["items"]
    print(apollo_items[0]["data"][0]["description"])
