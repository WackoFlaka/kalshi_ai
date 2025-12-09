# core/market_parser.py

def normalize_market(raw: dict) -> dict:
    """
    Convert the NEW Kalshi market JSON into a clean internal format
    used throughout the AI pipeline.
    """

    try:
        ticker = raw.get("ticker")
        title = raw.get("title", "")
        subtitle = raw.get("subtitle", "")

        yes_bid = raw.get("yes_bid", 0)
        yes_ask = raw.get("yes_ask", 0)
        no_bid = raw.get("no_bid", 0)
        no_ask = raw.get("no_ask", 0)

        market_type = raw.get("market_type", "binary")
        category = raw.get("category", "")
        rules = raw.get("rules_primary", "")

        close_time = raw.get("close_time")
        expiration_time = raw.get("expiration_time")

        return {
            "id": ticker,
            "title": title,
            "subtitle": subtitle,
            "question": title,     # AI uses this
            "yes_bid": yes_bid,
            "yes_ask": yes_ask,
            "no_bid": no_bid,
            "no_ask": no_ask,
            "market_type": market_type,
            "category": category,
            "rules": rules,
            "close_time": close_time,
            "expiration_time": expiration_time,
        }

    except Exception as e:
        print("❌ Error normalizing market:", e)
        return None
