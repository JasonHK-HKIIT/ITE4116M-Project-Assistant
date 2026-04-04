import os
from typing import Any

import requests


def _get_student_activities_endpoint() -> str:
    endpoint = os.getenv("MYPORTAL_ENDPOINT", "http://host.docker.internal:8000").strip()
    return f"{endpoint}/api/activities"


def _parse_limit(default_value: int = 5) -> int:
    raw_limit = os.getenv("MYPORTAL_STUDENT_ACTIVITIES_LIMIT", str(default_value))

    try:
        parsed_limit = int(raw_limit)
    except ValueError:
        return default_value

    return min(max(parsed_limit, 1), 20)


def _format_student_activities(keyword: str, data: list[dict[str, Any]]) -> str:
    keyword_label = keyword if keyword else "provided filters"

    if not data:
        return f'No student activities matched "{keyword_label}".'

    lines = f"Student activities matching \"{keyword_label}\":"

    for item in data:
        title = str(item.get("title") or "Untitled")
        activity_type = str(item.get("activity_type") or "Unknown type")
        execution_from = str(item.get("execution_from") or "Unknown")
        execution_to = str(item.get("execution_to") or "Unknown")
        campus_name = str(item.get("campus_name") or "Unknown campus")
        venue = str(item.get("venue") or "No venue specified")
        discipline = str(item.get("discipline") or "Unknown")
        has_vacancy = bool(item.get("has_vacancy"))
        description = str(item.get("description") or "No description available.").strip()

        lines += f"\n\n## {title}"
        lines += f"\nType: {activity_type}"
        lines += f"\nDate: {execution_from} to {execution_to}"
        lines += f"\nCampus: {campus_name}"
        lines += f"\nVenue: {venue}"
        lines += f"\nDiscipline: {discipline}"
        lines += f"\nVacancy: {'Available' if has_vacancy else 'Full'}"
        lines += f"\n\n{description}"

    return lines


def get_student_activities(
    keyword: str | None = None,
    activity_type: str | None = None,
    campus_id: int | None = None,
    discipline: str | None = None,
    locale: str | None = None,
    limit: int | None = None,
) -> str:
    normalized_keyword = (keyword or "").strip()

    normalized_limit = _parse_limit() if limit is None else min(max(limit, 1), 20)

    request_params: dict[str, Any] = {
        "limit": normalized_limit,
    }

    if normalized_keyword:
        request_params["keyword"] = normalized_keyword

    if activity_type:
        request_params["activity_type"] = activity_type
    if campus_id is not None:
        request_params["campus_id"] = campus_id
    if discipline:
        request_params["discipline"] = discipline
    if locale:
        request_params["locale"] = locale

    try:
        response = requests.get(
            _get_student_activities_endpoint(),
            params=request_params,
            timeout=10,
        )
    except requests.RequestException as exc:
        return f"Unable to reach the MyPortal student activities API: {exc}"

    if not response.ok:
        return (
            "MyPortal student activities API returned an error "
            f"({response.status_code})."
        )

    try:
        payload = response.json()
    except ValueError:
        return "MyPortal student activities API returned an invalid JSON response."

    data = payload.get("data")
    if not isinstance(data, list):
        return "MyPortal student activities API response did not include a valid data list."

    return _format_student_activities(keyword=normalized_keyword, data=data)
