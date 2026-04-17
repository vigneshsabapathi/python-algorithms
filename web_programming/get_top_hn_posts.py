"""
Fetch top stories from Hacker News via the Firebase REST API.

API docs: https://hacker-news.firebaseio.com/v0/
"""

from __future__ import annotations

import requests

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty"


def build_story_url(story_id: str | int) -> str:
    """
    Build the HackerNews item URL for a given story ID.

    >>> build_story_url(12345)
    'https://hacker-news.firebaseio.com/v0/item/12345.json?print=pretty'
    >>> build_story_url("99999")
    'https://hacker-news.firebaseio.com/v0/item/99999.json?print=pretty'
    """
    return HN_ITEM_URL.format(story_id=story_id)


def get_hackernews_story(story_id: str | int) -> dict:
    """
    Return a single HackerNews story as a dict.

    >>> isinstance(get_hackernews_story(1), dict)  # doctest: +SKIP
    True
    """
    return requests.get(build_story_url(story_id), timeout=10).json()


def hackernews_top_stories(max_stories: int = 10) -> list[dict]:
    """
    Return the top max_stories posts from HackerNews.

    >>> isinstance(hackernews_top_stories(5), list)  # doctest: +SKIP
    True
    """
    story_ids = requests.get(HN_TOP_STORIES_URL, timeout=10).json()[:max_stories]
    return [get_hackernews_story(story_id) for story_id in story_ids]


def hackernews_top_stories_as_markdown(max_stories: int = 10) -> str:
    """
    Return top HN stories formatted as a markdown list.

    >>> isinstance(hackernews_top_stories_as_markdown(3), str)  # doctest: +SKIP
    True
    """
    stories = hackernews_top_stories(max_stories)
    return "\n".join("* [{title}]({url})".format(**story) for story in stories)


if __name__ == "__main__":
    print(hackernews_top_stories_as_markdown())
