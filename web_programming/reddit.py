"""
Fetch posts from any subreddit via the Reddit JSON API.

Supports filtering by age ('new', 'top', 'hot') and selecting specific fields.
"""

from __future__ import annotations

import requests

REDDIT_BASE_URL = "https://www.reddit.com/r/{subreddit}/{age}.json?limit={limit}"

VALID_TERMS = set(
    """approved_at_utc approved_by author_flair_background_color
author_flair_css_class author_flair_richtext author_flair_template_id author_fullname
author_premium can_mod_post category clicked content_categories created_utc downs
edited gilded gildings hidden hide_score is_created_from_ads_ui is_meta
is_original_content is_reddit_media_domain is_video link_flair_css_class
link_flair_richtext link_flair_text link_flair_text_color media_embed mod_reason_title
name permalink pwls quarantine saved score secure_media secure_media_embed selftext
subreddit subreddit_name_prefixed subreddit_type thumbnail title top_awarded_type
total_awards_received ups upvote_ratio url user_reports""".split()
)


def build_reddit_url(subreddit: str, age: str = "new", limit: int = 1) -> str:
    """
    Build the Reddit JSON API URL for a subreddit.

    >>> build_reddit_url("python", "hot", 5)
    'https://www.reddit.com/r/python/hot.json?limit=5'
    >>> build_reddit_url("learnpython", "new", 1)
    'https://www.reddit.com/r/learnpython/new.json?limit=1'
    """
    return REDDIT_BASE_URL.format(subreddit=subreddit, age=age, limit=limit)


def get_subreddit_data(
    subreddit: str,
    limit: int = 1,
    age: str = "new",
    wanted_data: list | None = None,
) -> dict:
    """
    Return post data from a subreddit, optionally filtering to wanted_data fields.

    Raises ValueError for invalid field names.

    >>> get_subreddit_data("learnpython", wanted_data=["title", "url"])  # doctest: +SKIP
    {0: {'title': '...', 'url': '...'}}
    """
    wanted_data = wanted_data or []
    if invalid_search_terms := ", ".join(sorted(set(wanted_data) - VALID_TERMS)):
        raise ValueError(f"Invalid search term: {invalid_search_terms}")
    response = requests.get(
        build_reddit_url(subreddit, age, limit),
        headers={"User-agent": "A random string"},
        timeout=10,
    )
    response.raise_for_status()
    if response.status_code == 429:
        raise requests.HTTPError(response=response)
    data = response.json()
    if not wanted_data:
        return {idx: data["data"]["children"][idx] for idx in range(limit)}
    return {
        idx: {
            item: data["data"]["children"][idx]["data"][item]
            for item in wanted_data
        }
        for idx in range(limit)
    }


if __name__ == "__main__":
    print(
        get_subreddit_data(
            "learnpython", wanted_data=["title", "url", "selftext"]
        )
    )
