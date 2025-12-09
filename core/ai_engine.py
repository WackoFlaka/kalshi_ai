# core/ai_engine.py

import numpy as np
from fetchers.sentiment_fetcher import fetch_sentiment_score
from fetchers.news_fetcher import fetch_relevant_news
from models.ensemble_model import ensemble_predict


def generate_ai_probability(question: str, market: dict):
    """
    AI probability generator for Kalshi markets using:
      - Sentiment of the question text
      - News relevance
      - Market metadata (rules, type, category)
      - Ensemble ML model
    Returns a probability between 0 and 1.
    """

    # Extract extra features from the normalized market (new API)
    market_type = market.get("market_type", "")
    rules_text = market.get("rules", "")
    category = market.get("category", "")

    # NLP Sentiment scores
    sentiment_score = fetch_sentiment_score(question)

    # News relevance score
    news_factor = fetch_relevant_news(question)

    # Convert categorical fields into lightweight numerics
    type_flag = 1.0 if market_type == "binary" else 0.0
    category_flag = 1.0 if category else 0.0
    rules_length = len(rules_text) / 5000  # normalize to small number

    # Feature vector for ensemble model
    features = np.array([
        sentiment_score,
        news_factor,
        type_flag,
        category_flag,
        rules_length
    ], dtype=float)

    model_prob = ensemble_predict(features)

    # Clamp to safe 1–99%
    return max(0.01, min(0.99, float(model_prob)))
