def chunk_ppt_script(script_json: dict) -> list[dict]:
    """Chunks the PPT script into unified chunks for RAG or search systems."""
    chunks = []
    topic = script_json.get("topic", "")
    for slide in script_json.get("slides", []):
        chunk_text = f"Topic: {topic}\nSlide {slide.get('slide_no')}: {slide.get('title')}\nContent: {slide.get('content')}\nDetails: {slide.get('explanation')}"
        chunks.append({
            "chunk_id": f"slide_{slide.get('slide_no')}",
            "text": chunk_text,
            "slide_no": slide.get('slide_no'),
            "keywords": slide.get('keywords', [])
        })
    return chunks

def chunk_podcast_script(script_json: dict) -> list[dict]:
    """Chunks the Podcast dialogue down line by line into chunks."""
    chunks = []
    for idx, msg in enumerate(script_json.get("dialogue", [])):
        chunks.append({
            "chunk_id": f"dialogue_{idx}",
            "text": f"{msg.get('speaker')}: {msg.get('text')}",
            "speaker": msg.get('speaker')
        })
    return chunks
