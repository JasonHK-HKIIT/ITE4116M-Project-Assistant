import os
from datetime import datetime
from typing import Any

import requests


def _get_timetable_endpoint() -> str:
    endpoint = os.getenv("MYPORTAL_ENDPOINT", "http://host.docker.internal:8000").strip()
    return f"{endpoint}/api/timetable"


def _normalize_date(date_value: str | None) -> str | None:
    if not date_value:
        return None

    normalized = date_value.strip()
    if not normalized:
        return None

    return normalized


def _format_datetime(iso_value: str | None) -> str:
    if not iso_value:
        return "Unknown"

    try:
        parsed = datetime.fromisoformat(iso_value.replace("Z", "+00:00"))
    except ValueError:
        return iso_value

    return parsed.strftime("%Y-%m-%d %H:%M")


def _format_timetable(data: list[dict[str, Any]]) -> str:
    if not data:
        return "No timetable events were found for the selected date range."

    lines = "Your timetable events:"

    for event in data:
        title = str(event.get("title") or "Untitled event")
        event_type = str(event.get("type") or "unknown")
        source = str(event.get("source") or "calendar_event")
        start_at = _format_datetime(event.get("start_at"))
        end_at = _format_datetime(event.get("end_at"))
        location = str(event.get("location") or "No location")
        instructor = str(event.get("instructor") or "Not specified")

        lines += f"\n\n## {title}"
        lines += f"\n- Type: {event_type}"
        lines += f"\n- Source: {source}"
        lines += f"\n- Time: {start_at} to {end_at}"
        lines += f"\n- Location: {location}"
        lines += f"\n- Instructor: {instructor}"

    return lines


def get_timetable(
    user_id: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> str:
    if not user_id or not str(user_id).strip():
        return "Timetable tool is misconfigured: missing user_id."

    request_params: dict[str, Any] = {
        "user_id": str(user_id).strip(),
    }

    normalized_start_date = _normalize_date(start_date)
    normalized_end_date = _normalize_date(end_date)

    if normalized_start_date:
        request_params["start_date"] = normalized_start_date
    if normalized_end_date:
        request_params["end_date"] = normalized_end_date

    try:
        response = requests.get(
            _get_timetable_endpoint(),
            params=request_params,
            timeout=10,
        )
    except requests.RequestException as exc:
        return f"Unable to reach the MyPortal timetable API: {exc}"

    if not response.ok:
        return f"MyPortal timetable API returned an error ({response.status_code})."

    try:
        payload = response.json()
    except ValueError:
        return "MyPortal timetable API returned an invalid JSON response."

    data = payload.get("data")
    if not isinstance(data, list):
        return "MyPortal timetable API response did not include a valid data list."

    return _format_timetable(data)
