import logging
import asyncio
from typing import Optional
from ai_engine.tts.edge_tts_engine import generate_edge_tts
from ai_engine.tts.coqui_tts_engine import generate_coqui_tts
from ai_engine.tts.gtts_engine import generate_gtts
from storage.local_storage import ensure_job_directory

logger = logging.getLogger(__name__)

def sanitize_text(text: str, max_length: int = 4000) -> str:
    """Limits structural API payloads aggressively bypassing 429 timeouts strictly."""
    text = text.replace('\n', ' ').strip()
    return text[:max_length]

def generate_audio_manager(text: str, job_id: str, filename: str, subfolder: str = "audio", speaker: str = "Ziva") -> str:
    """
    Core Pipeline Logic strictly executing active fallbacks sequentially:
    1. Primary: Edge TTS (Highly Optimally Fast Async)
    2. Fallback A: Coqui TTS (Locally Native Processing)
    3. Fallback B: Google TTS (Absolutely Guaranteed Response)
    """
    safe_text = sanitize_text(text)
    
    # Establish filesystem structure mapping identically matching Frontend expectations
    job_dir = ensure_job_directory(job_id)
    audio_dir = job_dir / subfolder
    audio_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(audio_dir / filename)
    
    # Phase 1: High Velocity API Engine
    try:
        voice_id = "en-IN-PrabhatNeural" if speaker.upper() == "ZYRO" else "en-IN-NeerjaNeural"
        asyncio.run(generate_edge_tts(safe_text, output_path, voice=voice_id))
        return output_path
    except Exception as e:
        logger.warning(f"[TTS Route Check 1] Edge TTS heavily faulted: {e}. Resolving Fallback A (Coqui)...")
        
    # Phase 2: Local Processing Route natively executed
    try:
        generate_coqui_tts(safe_text, output_path)
        return output_path
    except Exception as e:
        logger.warning(f"[TTS Route Check 2] Coqui Model ML execution failed ({e}). Re-routing Fallback B (gTTS)...")
        
    # Phase 3: Unbreakable Sync Route
    try:
        generate_gtts(safe_text, output_path)
        return output_path
    except Exception as e:
        logger.error(f"[TTS Route 3] ALL PIPELINES FATALLY CRASHED. Audio completely rendered null: {e}")
        raise e
