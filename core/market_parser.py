# core/market_parser.py

class ParsedOutcome:
    def __init__(self, contract_id, ticker, yes_price, no_price, strike=None):
        self.contract_id = contract_id
        self.ticker = ticker
        self.yes_price = yes_price
        self.no_price = no_price
        self.strike = strike


class ParsedMarket:
    def __init__(self, market_id, title, mtype, outcomes):
        self.market_id = market_id
        self.title = title
        self.type = mtype
        self.outcomes = outcomes


def parse_kalshi_market(market_json, contracts_json):
    m = market_json["market"]

    outcomes = []

    for c in contracts_json.get("contracts", []):
        outcomes.append(
            ParsedOutcome(
                contract_id=c["id"],
                ticker=c.get("ticker"),
                yes_price=c.get("yes_bid"),
                no_price=c.get("no_ask"),
                strike=c.get("strike")
            )
        )

    return ParsedMarket(
        market_id=m["id"],
        title=m["title"],
        mtype=m["type"],
        outcomes=outcomes
    )
