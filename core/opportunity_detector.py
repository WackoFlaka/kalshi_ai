def identify_opportunity(fair_prob, market):
    """
    Determine whether the AI thinks it's a BUY YES, BUY NO, or NO EDGE.
    Uses yes_bid/no_bid from the normalized market format.
    """

    yes_price = market.get("yes_bid")  # price in cents
    no_price = market.get("no_bid")

    # If market is untradeable
    if yes_price is None or no_price is None:
        return "No price data"

    market_prob = yes_price / 100      # Convert cents → probability (0–1)
    edge = fair_prob - market_prob     # AI edge

    # AI sees BIG advantage → BUY YES
    if edge > 0.05:
        return f"BUY YES (edge: {edge:.2%})"

    # Market believes YES too strongly → AI thinks NO is underpriced
    elif edge < -0.05:
        return f"BUY NO (edge: {abs(edge):.2%})"

    return "No clear edge"
