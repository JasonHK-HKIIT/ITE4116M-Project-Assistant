from datetime import datetime, timezone

from app.tools import AvailableTools, TOOLS
from app.tools.current_time import get_current_time


class FixedDatetime(datetime):
    @classmethod
    def now(cls, tz=None):
        fixed_utc = datetime(2026, 4, 12, 0, 30, 45, tzinfo=timezone.utc)
        if tz is None:
            return fixed_utc.replace(tzinfo=None)
        return fixed_utc.astimezone(tz)


def test_get_current_time_uses_fixed_plus_8(monkeypatch):
    monkeypatch.setattr("app.tools.current_time.datetime", FixedDatetime)

    result = get_current_time()

    assert result == "2026-04-12 08:30:45"


def test_get_current_time_has_no_timezone_suffix():
    result = get_current_time()

    datetime.strptime(result, "%Y-%m-%d %H:%M:%S")
    assert "Z" not in result
    assert "+" not in result
    assert "UTC" not in result


def test_current_time_tool_is_registered():
    assert AvailableTools.CURRENT_TIME in TOOLS
