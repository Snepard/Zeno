from typing import Dict, List

from utils.cache import get_json, set_json


async def generate_slides(pdf_url: str, title: str) -> Dict:
    cache_key = f"lecture:slides:{pdf_url}:{title}"
    cached = get_json(cache_key)
    if cached:
        return cached

    slides: List[Dict] = []
    for i in range(1, 7):
        slides.append(
            {
                "slide_number": i,
                "title": f"{title} - Key Concept {i}",
                "bullets": [
                    f"Concept {i}.1 extracted from {pdf_url}",
                    f"Concept {i}.2 with practical insight",
                    "Summary point for learning retention",
                ],
                "speaker_notes": f"Narration script for slide {i}",
            }
        )

    result = {
        "slides": slides,
        "status": "partial",
    }
    set_json(cache_key, result, ttl_seconds=7200)
    return result


async def generate_slide_audio(job_id: str, slide_number: int, text: str) -> Dict:
    return {
        "job_id": job_id,
        "slide_number": slide_number,
        "audio_url": f"storage/audio/{job_id}/slide-{slide_number}.mp3",
        "status": "partial",
    }
