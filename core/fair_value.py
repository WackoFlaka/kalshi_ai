# core/fair_value.py

def compute_fair_value(kalshi_yes_price: float, ai_prob: float):
    """
    Combines market-implied probability with AI probability.
    YES price is in cents → convert to decimal.
    """

    market_prob = kalshi_yes_price / 100 if kalshi_yes_price else None

    if market_prob is None:
        return ai_prob

    # Weighted blend (AI has more confidence)
    fair = (ai_prob * 0.7) + (market_prob * 0.3)

    return max(0.01, min(0.99, fair))
