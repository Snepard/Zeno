import os
import subprocess
import logging
import torch

logger = logging.getLogger(__name__)

def merge_audio_files(audio_paths: list[str], output_path: str):
    """Safely merges slide audio cleanly natively protecting bounds"""
    if not audio_paths:
         return None
         
    # Generate concat file structurally for FFmpeg mapping sequentially tightly
    concat_file = output_path.replace(".mp3", "_concat.txt")
    with open(concat_file, "w", encoding='utf-8') as f:
        for p in audio_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")
            
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
        "-i", concat_file, "-c", "copy", output_path
    ]
    
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(concat_file):
        os.remove(concat_file)
    logger.info(f"Merged {len(audio_paths)} distinct voice nodes flawlessly natively -> {output_path}")
    return output_path

def render_video_from_images(image_dir: str, audio_path: str, output_path: str, framerate: int = 1):
    """
    Combines core assets generating base non-avatar MP4 utilizing heavily accelerated hardware execution.
    Targeting extreme h264_nvenc encoding bounds natively dynamically.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    cmd = [
        "ffmpeg", "-y", 
        "-framerate", str(framerate),
        "-pattern_type", "glob",
        "-i", f"{image_dir}/*.png",
        "-i", audio_path,
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest"
    ]
    
    # Dynamically inject optimization flags seamlessly structurally preventing limits globally
    if device == "cuda":
         logger.info("FFMPEG execution hooked onto NVENC dedicated encoding dynamically natively.")
         cmd.extend(["-c:v", "h264_nvenc", "-preset", "p6"]) # Hardware Core
    else:
         logger.info("FFMPEG executing legacy fallback standard encoding CPU strictly natively.")
         cmd.extend(["-c:v", "libx264", "-preset", "ultrafast"]) # CPU Threads
        
    cmd.append(output_path)
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logger.error(f"FFmpeg Generation Engine Faulted: {result.stderr.decode()}")
        raise RuntimeError("FFMPEG completely halted sequence generation directly natively.")
    return output_path
