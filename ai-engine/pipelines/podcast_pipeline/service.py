from typing import Dict, List

from utils.cache import get_json, set_json


async def generate_dialogue(pdf_url: str) -> Dict:
    cache_key = f"podcast:dialogue:{pdf_url}"
    cached = get_json(cache_key)
    if cached:
        return cached

    turns: List[Dict] = []
    for i in range(1, 9):
        speaker = "host_a" if i % 2 else "host_b"
        turns.append(
            {
                "turn": i,
                "speaker": speaker,
                "text": f"{speaker} discusses insight {i} from {pdf_url}",
            }
        )
    result = {"dialogue": turns, "status": "partial"}
    set_json(cache_key, result, ttl_seconds=7200)
    return result


async def synthesize_turn(job_id: str, turn: int, speaker: str, text: str) -> Dict:
    return {
        "job_id": job_id,
        "turn": turn,
        "speaker": speaker,
        "audio_url": f"storage/audio/{job_id}/turn-{turn}.mp3",
        "status": "partial",
    }
