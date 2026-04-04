import os
from typing import Any
from urllib.parse import urlparse
from textwrap import indent

import requests


def _get_news_endpoint() -> str:
    endpoint = os.getenv("MYPORTAL_ENDPOINT", "http://host.docker.internal:8000").strip()
    return f"{endpoint}/api/news"


def _parse_limit() -> int:
    raw_limit = os.getenv("MYPORTAL_NEWS_LIMIT", "5")

    try:
        parsed_limit = int(raw_limit)
    except ValueError:
        return 5

    return min(max(parsed_limit, 1), 20)


def _public_base_url() -> str | None:
    public_base_url = os.getenv("MYPORTAL_PUBLIC_ENDPOINT", "").strip()
    if not public_base_url:
        return None

    return public_base_url.rstrip("/")


def _normalize_news_url(url: Any, slug: str) -> str:
    fallback_path = f"/news/{slug}"
    if not url:
        raw_path = fallback_path
    else:
        raw_value = str(url)
        parsed = urlparse(raw_value)
        raw_path = parsed.path if (parsed.scheme or parsed.netloc) else raw_value
        if not raw_path:
            raw_path = fallback_path

    path = raw_path if raw_path.startswith("/") else f"/{raw_path}"

    public_base_url = _public_base_url()
    if public_base_url:
        return f"{public_base_url}{path}"

    if isinstance(url, str) and url:
        return url

    return path


def _format_news_items(keyword: str, data: list[dict[str, Any]]) -> str:
    if not data:
        return f'No latest news matched "{keyword}".'

    lines = f"Latest news matching \"{keyword}\":"

    for index, item in enumerate(data, start=1):
        title = str(item.get("title") or "Untitled")
        slug = str(item.get("slug") or "")
        published_on = str(item.get("published_on") or "Unknown date")
        content = str(item.get("content") or item.get("body") or item.get("summary") or "No content available.")
        url = _normalize_news_url(item.get("url"), slug)

        lines += f"\n\n## {title} ({published_on})\n\n"
        lines += content.rstrip().replace("\n", "\n\n")

        lines += f"\n\n{url}"

    return lines


def get_news_articles(query: str) -> str:
    keyword = query.strip()

    if not keyword:
        return "Please provide a keyword to search for the latest news."

    try:
        response = requests.get(
            _get_news_endpoint(),
            params={
                "keyword": keyword,
                "limit": _parse_limit(),
            },
            timeout=10,
        )
    except requests.RequestException as exc:
        return f"Unable to reach the MyPortal news articles API: {exc}"

    if not response.ok:
        return (
            "MyPortal news articles API returned an error "
            f"({response.status_code})."
        )

    try:
        payload = response.json()
    except ValueError:
        return "MyPortal news articles API returned an invalid JSON response."

    data = payload.get("data")
    if not isinstance(data, list):
        return "MyPortal news articles API response did not include a valid data list."

    return _format_news_items(keyword=keyword, data=data)
