import os
from typing import Any
from urllib.parse import urlparse

import requests


def _build_news_endpoint() -> str:
    hostname = os.getenv("MYPORTAL_BACKEND_HOSTNAME", "host.docker.internal:8000").strip()
    scheme = os.getenv("MYPORTAL_BACKEND_SCHEME", "http").strip()

    if hostname.startswith("http://") or hostname.startswith("https://"):
        base_url = hostname.rstrip("/")
    else:
        base_url = f"{scheme}://{hostname.strip('/')}"

    return f"{base_url}/api/news"


def _parse_limit() -> int:
    raw_limit = os.getenv("MYPORTAL_NEWS_LIMIT", "5")

    try:
        parsed_limit = int(raw_limit)
    except ValueError:
        return 5

    return min(max(parsed_limit, 1), 20)


def _parse_timeout() -> float:
    raw_timeout = os.getenv("MYPORTAL_BACKEND_TIMEOUT", "8")

    try:
        parsed_timeout = float(raw_timeout)
    except ValueError:
        return 8.0

    return max(parsed_timeout, 1.0)


def _public_base_url() -> str | None:
    public_base_url = os.getenv("MYPORTAL_PUBLIC_BASE_URL", "").strip()
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

    lines = [f'Latest news matching "{keyword}":']

    for index, item in enumerate(data, start=1):
        title = str(item.get("title") or "Untitled")
        slug = str(item.get("slug") or "")
        published_on = str(item.get("published_on") or "Unknown date")
        content = str(item.get("content") or item.get("body") or item.get("summary") or "No content available.")
        url = _normalize_news_url(item.get("url"), slug)

        lines.append(f"{index}. {title} ({published_on})")
        lines.append(f"   {content}")

        lines.append(f"   {url}")

    return "\n".join(lines)


def fetch_news_articles(query: str) -> str:
    keyword = query.strip()

    if not keyword:
        return "Please provide a keyword to search for the latest news."

    try:
        response = requests.get(
            _build_news_endpoint(),
            params={
                "keyword": keyword,
                "limit": _parse_limit(),
            },
            timeout=_parse_timeout(),
        )
    except requests.RequestException as exc:
        return f"Unable to reach the MyPortal backend news API: {exc}"

    if not response.ok:
        return (
            "MyPortal backend news API returned an error "
            f"({response.status_code})."
        )

    try:
        payload = response.json()
    except ValueError:
        return "MyPortal backend news API returned an invalid JSON response."

    data = payload.get("data")
    if not isinstance(data, list):
        return "MyPortal backend news API response did not include a valid data list."

    return _format_news_items(keyword=keyword, data=data)
