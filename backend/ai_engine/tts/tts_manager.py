import re
import logging
import asyncio
from ai_engine.tts.edge_tts_engine import generate_edge_tts
from ai_engine.tts.coqui_tts_engine import generate_coqui_tts
from ai_engine.tts.gtts_engine import generate_gtts
from storage.local_storage import ensure_job_directory

logger = logging.getLogger(__name__)

# Maps LaTeX patterns → natural speech
_LATEX_MAP = [
    (r"\\frac\{([^}]+)\}\{([^}]+)\}", r"\1 divided by \2"),
    (r"\\sqrt\{([^}]+)\}", r"square root of \1"),
    (r"\\cdot",    " times "),
    (r"\\times",   " times "),
    (r"\\pm",      " plus or minus "),
    (r"\\infty",   "infinity"),
    (r"\\alpha",   "alpha"),
    (r"\\beta",    "beta"),
    (r"\\gamma",   "gamma"),
    (r"\\delta",   "delta"),
    (r"\\theta",   "theta"),
    (r"\\lambda",  "lambda"),
    (r"\\mu",      "mu"),
    (r"\\pi",      "pi"),
    (r"\\sigma",   "sigma"),
    (r"\\omega",   "omega"),
    (r"\\sum",     "sum of"),
    (r"\\int",     "integral of"),
    (r"\\partial", "partial"),
    (r"\\nabla",   "gradient"),
    (r"\^2",       " squared"),
    (r"\^3",       " cubed"),
    (r"\^\{([^}]+)\}", r" to the power of \1"),
    (r"\^\{?(\w)\}?", r" to the power \1"),
    (r"_\{([^}]+)\}", r" subscript \1"),
    (r"_(\w)",     r" sub \1"),
    (r"\\left[\(\[]", ""),
    (r"\\right[\)\]]", ""),
    (r"\\mathbf\{([^}]+)\}", r"\1"),
    (r"\{|\}", ""),
    (r"\\", " "),
    (r"\s{2,}", " "),
]

def sanitize_text(text: str, max_length: int = 4000) -> str:
    """Strips LaTeX math notation into natural speech, then limits length."""
    cleaned = text.replace('\n', ' ').strip()
    for pattern, replacement in _LATEX_MAP:
        cleaned = re.sub(pattern, replacement, cleaned)
    return cleaned[:max_length].strip()


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
