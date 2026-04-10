import logging
from moviepy.editor import AudioFileClip

logger = logging.getLogger(__name__)

def get_audio_duration(audio_path: str) -> float:
    try:
        # Utilizing moviepy's native underlying imageio-ffmpeg wrapper which contains bundled binaries 
        # completely bypassing pydub/system-ffprobe strict PATH requirements on Windows. 
        clip = AudioFileClip(audio_path)
        if clip.duration is None:
            dur = 10.0
        else:
            dur = float(clip.duration)
        clip.close()
        return dur
    except Exception as e:
        logger.error(f"Failed to get audio duration for {audio_path}: {e}")
        return 10.0

def build_timeline(scenes: list, job_dir: str) -> dict:
    """Builds alignment map mapping scenes to audio logic."""
    timeline = []
    
    for scene in scenes:
        audio_path = f"{job_dir}/audio/scene_{scene['scene_id']}.mp3"
        video_path = f"{job_dir}/scenes/scene_{scene['scene_id']}.mp4"
        
        # Pull exact audio duration to synchronize
        actual_duration = get_audio_duration(audio_path)
        
        timeline.append({
            "scene_id": scene['scene_id'],
            "audio_path": audio_path,
            "video_path": video_path,
            "duration": actual_duration
        })
        
    return {"timeline": timeline}
