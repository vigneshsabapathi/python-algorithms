"""
Search gogoanime for anime, list episodes, and return stream/download URLs.

Scrapes ww7.gogoanime2.org for anime search results and episode links.
"""

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

BASE_URL = "https://ww7.gogoanime2.org"


def search_scraper(anime_name: str) -> list:
    """
    Return a list of anime dicts with 'title' and 'url' keys.

    >>> type(search_scraper("demon_slayer"))  # doctest: +SKIP
    <class 'list'>
    """
    search_url = f"{BASE_URL}/search?keyword={anime_name}"
    response = requests.get(
        search_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    anime_ul = soup.find("ul", {"class": "items"})
    if anime_ul is None or isinstance(anime_ul, NavigableString):
        raise ValueError(f"Could not find any anime with name {anime_name}")
    anime_list = []
    for anime in anime_ul.children:
        if isinstance(anime, Tag):
            anime_url = anime.find("a")
            anime_title = anime.find("a")
            if anime_url is None or isinstance(anime_url, NavigableString):
                continue
            if anime_title is None or isinstance(anime_title, NavigableString):
                continue
            anime_list.append(
                {"title": anime_title["title"], "url": anime_url["href"]}
            )
    return anime_list


def search_anime_episode_list(episode_endpoint: str) -> list:
    """
    Return a list of episode dicts with 'title' and 'url' for an anime endpoint.

    >>> type(search_anime_episode_list("/anime/kimetsu-no-yaiba"))  # doctest: +SKIP
    <class 'list'>
    """
    request_url = f"{BASE_URL}{episode_endpoint}"
    response = requests.get(
        url=request_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    episode_page_ul = soup.find("ul", {"id": "episode_related"})
    if episode_page_ul is None or isinstance(episode_page_ul, NavigableString):
        raise ValueError(f"Could not find any episodes for {episode_endpoint}")
    episode_list = []
    for episode in episode_page_ul.children:
        if isinstance(episode, Tag):
            url = episode.find("a")
            title = episode.find("div", {"class": "name"})
            if url is None or isinstance(url, NavigableString):
                continue
            if title is None or isinstance(title, NavigableString):
                continue
            episode_list.append(
                {"title": title.text.replace(" ", ""), "url": url["href"]}
            )
    return episode_list


def get_anime_episode(episode_endpoint: str) -> list:
    """
    Return [watch_url, download_url] for a given episode endpoint.

    >>> type(get_anime_episode("/watch/kimetsu-no-yaiba/1"))  # doctest: +SKIP
    <class 'list'>
    """
    episode_page_url = f"{BASE_URL}{episode_endpoint}"
    response = requests.get(
        url=episode_page_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    url_tag = soup.find("iframe", {"id": "playerframe"})
    if url_tag is None or isinstance(url_tag, NavigableString):
        raise RuntimeError(f"Could not find player iframe for {episode_endpoint}")
    episode_url = url_tag["src"]
    if not isinstance(episode_url, str):
        raise RuntimeError(f"Could not get episode URL for {episode_endpoint}")
    download_url = episode_url.replace("/embed/", "/playlist/") + ".m3u8"
    return [f"{BASE_URL}{episode_url}", f"{BASE_URL}{download_url}"]


if __name__ == "__main__":
    anime_name = input("Enter anime name: ").strip()
    anime_list = search_scraper(anime_name)
    if not anime_list:
        print("No anime found with this name.")
    else:
        print(f"Found {len(anime_list)} results:")
        for i, anime in enumerate(anime_list, 1):
            print(f"{i}. {anime['title']}")
        choice = int(input("Choose an anime: ").strip())
        chosen = anime_list[choice - 1]
        print(f"You chose {chosen['title']}. Searching for episodes...")
        episode_list = search_anime_episode_list(chosen["url"])
        if not episode_list:
            print("No episodes found.")
        else:
            print(f"Found {len(episode_list)} episodes:")
            for i, ep in enumerate(episode_list, 1):
                print(f"{i}. {ep['title']}")
            ep_choice = int(input("Choose an episode: ").strip())
            chosen_ep = episode_list[ep_choice - 1]
            watch_url, dl_url = get_anime_episode(chosen_ep["url"])
            print(f"\nTo watch: {watch_url}")
            print(f"To download: {dl_url}")
