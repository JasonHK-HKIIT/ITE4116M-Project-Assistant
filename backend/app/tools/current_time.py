from datetime import datetime, timedelta, timezone

TARGET_TIMEZONE = timezone(timedelta(hours=8))


def get_current_time() -> str:
    now_in_utc = datetime.now(timezone.utc)
    now_in_target_timezone = now_in_utc.astimezone(TARGET_TIMEZONE)
    return now_in_target_timezone.strftime("%Y-%m-%d %H:%M:%S")
