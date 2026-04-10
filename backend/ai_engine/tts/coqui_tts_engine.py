import logging
import httpx
import os

logger = logging.getLogger(__name__)

TTS_SERVICE_URL = "http://127.0.0.1:8001/generate-audio"

def generate_coqui_tts(text: str, output_path: str) -> str:
    """
    Microservice Client architecture natively deployed. 
    Protects the central FastAPI Node completely against NumPy C-binding corruptions
    by explicitly bridging inference routing via HTTP to the localized Sub-Server Sandbox.
    """
    logger.info(f"Generating Coqui VITS TTS over secure internal Microservice Sandboxed Node: {output_path}")
    
    try:
        # Generate Absolute path strictly avoiding directory resolution gaps inside separate environments
        abs_output_path = os.path.abspath(output_path)
        
        response = httpx.post(TTS_SERVICE_URL, json={
            "text": text,
            "output_path": abs_output_path
        }, timeout=45.0)
        
        response.raise_for_status()
        
        if response.status_code == 200:
            return abs_output_path
            
    except Exception as e:
        logger.error(f"Coqui microservice strictly unavailable. Pipeline gracefully returning exception hook: {e}")
        raise e
