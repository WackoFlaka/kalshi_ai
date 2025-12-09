# core/opportunity_detector.py

def identify_opportunity(fair_prob, market_outcome):
    yes_price = market_outcome.yes_price

    if yes_price is None:
        return "No price data available"

    market_prob = yes_price / 100
    edge = fair_prob - market_prob

    if edge > 0.05:
        return f"BUY YES (edge: {edge:.2%})"
    elif edge < -0.05:
        return f"BUY NO (edge: {abs(edge):.2%})"
    else:
        return "No clear edge"
