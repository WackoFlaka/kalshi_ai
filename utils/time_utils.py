# utils/time_utils.py

from datetime import datetime, timezone


def parse_kalshi_timestamp(ts: str) -> datetime:
    """
    Kalshi timestamps look like:
    '2025-01-13T23:59:59Z'
    """
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except Exception:
        return datetime.now(timezone.utc)


def hours_until(expiration: datetime) -> float:
    now = datetime.now(timezone.utc)
    delta = expiration - now
    return max(0, delta.total_seconds() / 3600)


def urgency_multiplier(hours_left: float) -> float:
    """
    Markets behave differently near expiration.
    1.0 = normal  
    1.3+ = heightened volatility  
    """
    if hours_left < 6:
        return 1.4
    if hours_left < 24:
        return 1.2
    return 1.0
