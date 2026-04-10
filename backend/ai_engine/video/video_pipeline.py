import os
import json
import logging
from ai_engine.video.ffmpeg_utils import merge_audio_files
from storage.local_storage import ensure_job_directory

logger = logging.getLogger(__name__)

def generate_master_video(job_id: str):
    """
    Deep execution core traversing raw independent output nodes merging structures intelligently tracking
    strict logic generation bounds explicitly.
    """
    logger.info(f"Aggregating distributed Audio architectures strictly merging structurally native: Job {job_id}")
    
    job_dir = ensure_job_directory(job_id)
    script_path = job_dir / "script.json"
    
    if not script_path.exists():
        raise FileNotFoundError(f"Video Flow failed strictly identifying primary script structurally ({job_id}).")
        
    with open(script_path, "r") as f:
        script = json.load(f)
        
    slides = script.get("slides", [])
    
    # 1. Synthesize localized output arrays logically securely tracking exact ordering globally
    audio_paths = []
    for s in slides:
        a_url = s.get("audio_url")
        if a_url:
             file_path = str(job_dir / "audio" / os.path.basename(a_url))
             if os.path.exists(file_path):
                 audio_paths.append(file_path)
                 
    # 2. Re-Format execution strictly natively binding FFmpeg correctly
    audio_dir = job_dir / "audio"
    full_audio = str(audio_dir / "full_audio.mp3")
    
    if audio_paths:
        merge_audio_files(audio_paths, full_audio)
    else:
        logger.warning("No localized audio nodes found securely natively resolving empty video architecture!")
    
    return {
        "full_audio": full_audio,
        "video_status": "scenes_ready"
    }
