# core/category_classifier.py

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

CATEGORIES = [
    "politics",
    "sports",
    "crypto",
    "economics",
    "companies",
    "world",
    "technology",
    "health",
    "climate",
    "events"
]


def classify_category(text):
    """Return the closest matching market category."""
    embeddings = model.encode([text] + CATEGORIES, convert_to_tensor=True)
    query_emb = embeddings[0]
    cat_embs = embeddings[1:]

    similarities = util.cos_sim(query_emb, cat_embs)[0]
    best_index = int(similarities.argmax())

    return CATEGORIES[best_index]
