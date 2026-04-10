from unittest.mock import Mock

from app.tools.user_profile import get_user_profile


def test_fetch_user_profile_success_with_student(monkeypatch):
    captured = {}

    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "data": {
            "user": {
                "username": "240155170",
                "family_name": "Chan",
                "given_name": "Tai Man",
                "role": "student",
                "avatar_url": "https://example.com/avatar.jpg",
            },
            "student": {
                "institute": {"name": "HKIIT"},
                "campus": {"name": "IVE (LWL)"},
                "gender": "male",
                "date_of_birth": "2001-02-03",
                "nationality": "Chinese",
                "mother_tongue": "Cantonese",
                "mobile_no": "91234567",
                "tel_no": "26360000",
                "address": "Some Address",
                "current_class": {"class_code": "IT114105", "academic_year": 2025},
                "programmes": [
                    {"programme_code": "HDSE", "name": "Higher Diploma in Software Engineering"}
                ],
            },
        }
    }

    def _mock_get(*args, **kwargs):
        captured["params"] = kwargs.get("params", {})
        return mock_response

    monkeypatch.setattr("requests.get", _mock_get)

    result = get_user_profile(user_id="123", locale="en")

    assert "Your profile" in result
    assert "Username: 240155170" in result
    assert "Student details" in result
    assert "Current class: IT114105 (2025)" in result
    assert "HDSE: Higher Diploma in Software Engineering" in result
    assert captured["params"]["user_id"] == "123"
    assert captured["params"]["locale"] == "en"


def test_fetch_user_profile_success_without_student(monkeypatch):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "data": {
            "user": {
                "username": "staff01",
                "family_name": "Lee",
                "given_name": "Admin",
                "role": "staff",
            }
        }
    }

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_user_profile(user_id="11")

    assert "Role: staff" in result
    assert "No student record is available" in result


def test_fetch_user_profile_handles_backend_error(monkeypatch):
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 503

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_user_profile(user_id="11")

    assert "returned an error (503)" in result


def test_fetch_user_profile_handles_invalid_payload(monkeypatch):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {"unexpected": "shape"}

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_user_profile(user_id="11")

    assert "did not include a valid data object" in result
