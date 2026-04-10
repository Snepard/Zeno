import logging
import torch

logger = logging.getLogger(__name__)

# System delays PyTorch bootstrapping lazily avoiding locking Uvicorn RAM upon boot cycle
TTS_MODEL = None
use_cuda = torch.cuda.is_available()

def get_coqui_tts():
    global TTS_MODEL
    if TTS_MODEL is None:
        try:
            # Importing locally scoped Coqui structural libraries manually
            from TTS.api import TTS
            # Loading VCTK VITS models safely natively onto explicit CUDA bounds avoiding cpu faults globally
            logger.info(f"Allocating localized Core Model bounds natively deploying GPU {'ENABLED' if use_cuda else 'DISABLED'}")
            TTS_MODEL = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=use_cuda)
        except ImportError:
            logger.error("Coqui TTS strictly unavailable inside local environment. Execute `pip install TTS`.")
            raise ImportError("Critical ML Voice Engine unavailable")
    return TTS_MODEL

def generate_coqui_tts(text: str, output_path: str) -> str:
    """Guarantees local audio execution mapping locally inside container bypassing APIs completely."""
    logger.info(f"Generating local Coqui VITS engine TTS natively checking constraints: {output_path}")
    tts = get_coqui_tts()
    tts.tts_to_file(text=text, file_path=output_path, speaker=tts.speakers[0] if tts.speakers else None)
    
    # Securely flush rendering contexts strictly globally preventing heavy VRAM overflows!
    if use_cuda:
        torch.cuda.empty_cache()
        
    return output_path
