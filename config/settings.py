from dotenv import load_dotenv
import os

load_dotenv()

KALSHI_API_KEY_ID = os.getenv("KALSHI_API_KEY_ID")
KALSHI_API_SECRET = os.getenv("KALSHI_API_SECRET")

BASE_URL = "https://api.kalshi.com/trade-api/v2"

if not KALSHI_API_KEY_ID or not KALSHI_API_SECRET:
    raise Exception("Missing Kalshi API credentials in .env")
