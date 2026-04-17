"""
Send a message to a Slack channel via an Incoming Webhook URL.

Create a webhook at: https://my.slack.com/services/new/incoming-webhook/
"""

import requests

CONTENT_TYPE_JSON = "application/json"


def send_slack_message(message_body: str, slack_url: str) -> None:
    """
    POST a message to a Slack incoming webhook URL.

    Raises ValueError if Slack returns a non-200 status.

    >>> send_slack_message("Hello!", "https://hooks.slack.com/services/invalid")  # doctest: +SKIP
    Traceback (most recent call last):
        ...
    ValueError: Request to slack returned an error 403...
    """
    headers = {"Content-Type": CONTENT_TYPE_JSON}
    response = requests.post(
        slack_url, json={"text": message_body}, headers=headers, timeout=10
    )
    if response.status_code != 200:
        raise ValueError(
            f"Request to slack returned an error {response.status_code}, "
            f"the response is:\n{response.text}"
        )


if __name__ == "__main__":
    import os

    slack_url = os.getenv("SLACK_WEBHOOK_URL", "")
    if not slack_url:
        raise KeyError("Set SLACK_WEBHOOK_URL environment variable first.")
    message = input("Enter message: ").strip()
    send_slack_message(message, slack_url)
    print("Message sent successfully.")
