import os
from typing import Any

import requests


def _get_profile_endpoint() -> str:
    endpoint = os.getenv("MYPORTAL_ENDPOINT", "http://host.docker.internal:8000").strip()
    return f"{endpoint}/api/profile"


def _normalize_locale(locale: str | None) -> str:
    if locale and locale.strip():
        return locale.strip()

    return os.getenv("MYPORTAL_PROFILE_LOCALE", "en").strip() or "en"


def _format_user_profile(data: dict[str, Any]) -> str:
    user = data.get("user") if isinstance(data.get("user"), dict) else {}
    student = data.get("student") if isinstance(data.get("student"), dict) else None

    role = str(user.get("role") or "unknown")
    full_name = " ".join(
        part for part in [str(user.get("family_name") or "").strip(), str(user.get("given_name") or "").strip()] if part
    ).strip()
    if not full_name:
        full_name = str(user.get("username") or "Unknown user")

    lines = "Your profile:\n"
    lines += f"- Name: {full_name}"
    lines += f"\n- Username: {str(user.get('username') or 'N/A')}"
    lines += f"\n- Role: {role}"

    chinese_name = str(user.get("chinese_name") or "").strip()
    if chinese_name:
        lines += f"\n- Chinese name: {chinese_name}"

    avatar_url = str(user.get("avatar_url") or "").strip()
    if avatar_url:
        lines += f"\n- Avatar: {avatar_url}"

    if not student:
        return lines + "\n\nNo student record is available for this account."

    institute = student.get("institute") if isinstance(student.get("institute"), dict) else {}
    campus = student.get("campus") if isinstance(student.get("campus"), dict) else {}
    current_class = student.get("current_class") if isinstance(student.get("current_class"), dict) else {}

    lines += "\n\nStudent details:"
    lines += f"\n- Institute: {str(institute.get('name') or 'N/A')}"
    lines += f"\n- Campus: {str(campus.get('name') or 'N/A')}"
    lines += f"\n- Gender: {str(student.get('gender') or 'N/A')}"
    lines += f"\n- Date of birth: {str(student.get('date_of_birth') or 'N/A')}"
    lines += f"\n- Nationality: {str(student.get('nationality') or 'N/A')}"
    lines += f"\n- Mother tongue: {str(student.get('mother_tongue') or 'N/A')}"
    lines += f"\n- Mobile no: {str(student.get('mobile_no') or 'N/A')}"
    lines += f"\n- Telephone no: {str(student.get('tel_no') or 'N/A')}"
    lines += f"\n- Address: {str(student.get('address') or 'N/A')}"

    class_code = str(current_class.get("class_code") or "N/A")
    academic_year = str(current_class.get("academic_year") or "N/A")
    lines += f"\n- Current class: {class_code} ({academic_year})"

    programmes = student.get("programmes")
    if isinstance(programmes, list) and programmes:
        lines += "\n- Programmes:"
        for programme in programmes:
            if not isinstance(programme, dict):
                continue
            code = str(programme.get("programme_code") or "N/A")
            name = str(programme.get("name") or "Unnamed programme")
            lines += f"\n  - {code}: {name}"

    return lines


def get_user_profile(user_id: str, locale: str | None = None) -> str:
    if not user_id or not str(user_id).strip():
        return "User profile tool is misconfigured: missing user_id."

    request_params: dict[str, Any] = {
        "user_id": str(user_id).strip(),
        "locale": _normalize_locale(locale),
    }

    try:
        response = requests.get(
            _get_profile_endpoint(),
            params=request_params,
            timeout=10,
        )
    except requests.RequestException as exc:
        return f"Unable to reach the MyPortal profile API: {exc}"

    if not response.ok:
        return f"MyPortal profile API returned an error ({response.status_code})."

    try:
        payload = response.json()
    except ValueError:
        return "MyPortal profile API returned an invalid JSON response."

    data = payload.get("data")
    if not isinstance(data, dict):
        return "MyPortal profile API response did not include a valid data object."

    return _format_user_profile(data)
