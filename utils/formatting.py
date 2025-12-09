# utils/formatting.py

def pct(value: float) -> str:
    """
    Convert a float probability (0–1) into a clean percentage string.
    Example: 0.34 → "34%"
    """
    return f"{value * 100:.1f}%"


def price_to_prob(price_cents: int) -> float:
    """
    Convert Kalshi YES price (0–99 cents) into probability (0–1).
    """
    return max(0.0, min(1.0, price_cents / 100.0))


def prob_to_price(prob: float) -> int:
    """
    Convert decimal probability into Kalshi-style cents.
    """
    return int(prob * 100)
