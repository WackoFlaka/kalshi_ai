# Kalshi AI — API Usage Guide

This project connects to the Kalshi Trade API to read:

- Markets
- Contracts
- YES/NO prices
- Multi-outcome markets
- Metadata

## Basic Example

```python
from core.kalshi_client import KalshiClient

client = KalshiClient()
markets = client.list_markets()

print(markets)
