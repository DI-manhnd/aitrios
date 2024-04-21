from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), "JST")


def convert_unixtime_to_datetime(unix_timestamp: int):
    if unix_timestamp == 0:
        return None

    unix_timestamp_sec = unix_timestamp // 1000
    unix_timestamp_ms = unix_timestamp % 1000

    dt = datetime.fromtimestamp(unix_timestamp_sec, JST)
    dt = dt.replace(microsecond=unix_timestamp_ms * 1000)
    return dt
