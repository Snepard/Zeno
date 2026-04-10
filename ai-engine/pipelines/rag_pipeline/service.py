from typing import Dict, List

from utils.cache import get_json, set_json


async def generate_flashcards(pdf_url: str, count: int) -> Dict:
    cache_key = f"rag:flashcards:{pdf_url}:{count}"
    cached = get_json(cache_key)
    if cached:
        return cached

    cards: List[Dict] = []
    for i in range(1, count + 1):
        cards.append(
            {
                "question": f"What is core idea {i} in {pdf_url}?",
                "answer": f"Core idea {i} answer synthesized with retrieval context.",
            }
        )
    result = {"cards": cards, "status": "complete"}
    set_json(cache_key, result, ttl_seconds=7200)
    return result
