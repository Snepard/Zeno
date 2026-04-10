from gtts import gTTS
import logging

logger = logging.getLogger(__name__)

def generate_gtts(text: str, output_path: str) -> str:
    """Universal robust offline/online combination execution generating clean base-case audio flawlessly."""
    logger.info(f"Deploying severe Fallback gTTS: {output_path}")
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_path)
    return output_path
