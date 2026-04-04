from unittest.mock import Mock

from app.tools.news_articles import get_news_articles


def test_fetch_news_articles_success(monkeypatch):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "data": [
            {
                "title": "Exam Schedule Released",
                "published_on": "2026-04-01",
                "content": "The final exam schedule is now available with full article details.",
                "url": "http://portal.local/news/exam-schedule",
            }
        ]
    }

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_news_articles("exam")

    assert 'Latest news matching "exam":' in result
    assert "Exam Schedule Released (2026-04-01)" in result
    assert "The final exam schedule is now available with full article details." in result


def test_fetch_news_articles_handles_backend_error(monkeypatch):
    mock_response = Mock()
    mock_response.ok = False
    mock_response.status_code = 503

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_news_articles("portal")

    assert "returned an error (503)" in result


def test_fetch_news_articles_handles_invalid_payload(monkeypatch):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {"unexpected": "shape"}

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

    result = get_news_articles("notice")

    assert "did not include a valid data list" in result


def test_fetch_news_articles_rewrites_links_with_public_base_url(monkeypatch):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "data": [
            {
                "slug": "exam-schedule",
                "title": "Exam Schedule Released",
                "published_on": "2026-04-01",
                "content": "The final exam schedule is now available with full article details.",
                "url": "http://host.docker.internal:8000/news/exam-schedule",
            }
        ]
    }

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)
    monkeypatch.setenv("MYPORTAL_PUBLIC_ENDPOINT", "https://portal.vtc.edu.hk")

    result = get_news_articles("exam")

    assert "https://portal.vtc.edu.hk/news/exam-schedule" in result
