import edge_tts
import asyncio
import logging

logger = logging.getLogger(__name__)

async def generate_edge_tts(text: str, output_path: str, voice: str = "en-US-AriaNeural") -> str:
    """Async execution layer directly binding Microsoft Edge Azure Cognitive Services TTS optimally."""
    logger.info(f"Generating Edge TTS sequence natively: {output_path}")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    return output_path
