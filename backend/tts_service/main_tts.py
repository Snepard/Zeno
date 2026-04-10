from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from TTS.api import TTS
import logging
import torch
import os

logger = logging.getLogger("TTS_Microservice")
app = FastAPI(title="Zeno TTS Microservice")

# Global TTS model boots natively onto CUDA sequentially avoiding memory locks
try:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts_model = TTS("tts_models/en/ljspeech/vits").to(device)
    logger.info(f"Loaded Coqui TTS Model natively onto {device}")
except Exception as e:
    logger.error(f"Failed to boot TTS node initially: {e}")
    tts_model = None

class TTSRequest(BaseModel):
    text: str
    output_path: str

@app.get("/")
def read_root():
    return {"status": "online", "service": "Zeno TTS Microservice"}

@app.post("/generate-audio")
def generate_audio(payload: TTSRequest):
    if not tts_model:
        raise HTTPException(status_code=503, detail="TTS Model is strictly offline due to native errors.")
        
    try:
        # Create output directories safely resolving path bounds
        os.makedirs(os.path.dirname(payload.output_path), exist_ok=True)
        
        tts_model.tts_to_file(text=payload.text, file_path=payload.output_path)
        return {"status": "success", "file": payload.output_path}
    except Exception as e:
        logger.error(f"TTS Synthesis Failed natively: {e}")
        raise HTTPException(status_code=500, detail=str(e))
