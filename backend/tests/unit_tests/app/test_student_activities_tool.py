from unittest.mock import Mock

from app.tools.student_activities import get_student_activities


def test_fetch_student_activities_success(monkeypatch):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "data": [
            {
                "title": "Coding Club Meetup",
                "activity_type": "Student Groups",
                "execution_from": "2026-04-10",
                "execution_to": "2026-04-12",
                "campus_name": "Main Campus",
                "venue": "Lab 301",
                "discipline": "IT",
                "has_vacancy": True,
                "description": "Hands-on coding practice for students.",
            }
        ]
    }

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_student_activities(keyword="coding")

    assert 'Student activities matching "coding":' in result
    assert "Coding Club Meetup" in result
    assert "Type: Student Groups" in result
    assert "Vacancy: Available" in result


def test_fetch_student_activities_handles_backend_error(monkeypatch):
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 503

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_student_activities(keyword="coding")

    assert "returned an error (503)" in result


def test_fetch_student_activities_handles_invalid_payload(monkeypatch):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {"unexpected": "shape"}

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_student_activities(keyword="coding")

    assert "did not include a valid data list" in result


def test_fetch_student_activities_accepts_empty_keyword(monkeypatch):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {"data": []}

    captured = {}

    def _mock_get(*args, **kwargs):
        captured["params"] = kwargs.get("params", {})
        return mock_response

    monkeypatch.setattr("requests.get", _mock_get)

    result = get_student_activities(keyword="   ", activity_type="Student Groups")

    assert "provided filters" in result
    assert "keyword" not in captured["params"]
    assert captured["params"]["activity_type"] == "Student Groups"


def test_fetch_student_activities_uses_explicit_optional_filters(monkeypatch):
    captured = {}

    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {"data": []}

    def _mock_get(*args, **kwargs):
        captured["params"] = kwargs.get("params", {})
        return mock_response

    monkeypatch.setattr("requests.get", _mock_get)

    get_student_activities(
        keyword="coding",
        activity_type="Student Groups",
        campus_id=1,
        discipline="IT",
        locale="en",
        limit=2,
    )

    assert captured["params"]["keyword"] == "coding"
    assert captured["params"]["activity_type"] == "Student Groups"
    assert captured["params"]["campus_id"] == 1
    assert captured["params"]["discipline"] == "IT"
    assert captured["params"]["locale"] == "en"
    assert captured["params"]["limit"] == 2
