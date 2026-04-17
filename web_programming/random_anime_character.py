"""
Fetch a random anime character from mywaifulist.moe and save their image.

Scrapes og:title, og:image, and #description from the random character page.
"""

import os

import requests
from bs4 import BeautifulSoup

RANDOM_CHARACTER_URL = "https://www.mywaifulist.moe/random"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def save_image(image_url: str, image_title: str) -> None:
    """
    Download image from image_url and save to image_title filename.

    >>> save_image("https://example.com/img.jpg", "test.jpg")  # doctest: +SKIP
    """
    image = requests.get(image_url, headers=HEADERS, timeout=10)
    with open(image_title, "wb") as file:
        file.write(image.content)


def random_anime_character() -> tuple[str, str, str]:
    """
    Return (title, description, image_filename) for a random anime character.

    >>> title, desc, img = random_anime_character()  # doctest: +SKIP
    >>> isinstance(title, str)  # doctest: +SKIP
    True
    """
    soup = BeautifulSoup(
        requests.get(RANDOM_CHARACTER_URL, headers=HEADERS, timeout=10).text,
        "html.parser",
    )
    title = soup.find("meta", attrs={"property": "og:title"}).attrs["content"]
    image_url = soup.find("meta", attrs={"property": "og:image"}).attrs["content"]
    description = soup.find("p", id="description").get_text()
    _, image_extension = os.path.splitext(os.path.basename(image_url))
    image_title = title.strip().replace(" ", "_") + image_extension
    save_image(image_url, image_title)
    return title, description, image_title


if __name__ == "__main__":
    title, desc, image_title = random_anime_character()
    print(f"{title}\n\n{desc}\n\nImage saved: {image_title}")
