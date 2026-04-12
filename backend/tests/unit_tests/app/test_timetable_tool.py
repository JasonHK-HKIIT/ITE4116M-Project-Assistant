from unittest.mock import Mock

from app.tools.timetable import get_timetable


def test_fetch_timetable_success(monkeypatch):
    captured = {}

    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "data": [
            {
                "title": "COMP1001",
                "type": "class",
                "source": "class_timetable",
                "start_at": "2026-04-15T09:00:00+00:00",
                "end_at": "2026-04-15T10:00:00+00:00",
                "location": "Room 301",
                "instructor": "Chan Tai Man",
            }
        ]
    }

    def _mock_get(*args, **kwargs):
        captured["params"] = kwargs.get("params", {})
        return mock_response

    monkeypatch.setattr("requests.get", _mock_get)

    result = get_timetable(user_id="123", start_date="2026-04-01", end_date="2026-04-30")

    assert "Your timetable events" in result
    assert "COMP1001" in result
    assert "Type: class" in result
    assert captured["params"]["user_id"] == "123"
    assert captured["params"]["start_date"] == "2026-04-01"
    assert captured["params"]["end_date"] == "2026-04-30"


def test_fetch_timetable_handles_backend_error(monkeypatch):
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 503

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_timetable(user_id="11")

    assert "returned an error (503)" in result


def test_fetch_timetable_handles_invalid_payload(monkeypatch):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {"unexpected": "shape"}

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_timetable(user_id="11")

    assert "did not include a valid data list" in result


def test_fetch_timetable_omits_empty_dates(monkeypatch):
    captured = {}

    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {"data": []}

    def _mock_get(*args, **kwargs):
        captured["params"] = kwargs.get("params", {})
        return mock_response

    monkeypatch.setattr("requests.get", _mock_get)

    result = get_timetable(user_id="11", start_date="  ", end_date=None)

    assert "No timetable events" in result
    assert captured["params"] == {"user_id": "11"}
