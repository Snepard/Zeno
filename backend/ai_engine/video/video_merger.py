import logging
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import gc

logger = logging.getLogger(__name__)

def merge_timeline(timeline: dict, output_path: str) -> str:
    import os
    import subprocess
    import imageio_ffmpeg
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    job_dir = os.path.dirname(output_path)
    concat_file = os.path.join(job_dir, "concat_list.txt")
    chunk_files = []
    
    try:
        # Phase 1: Mux raw Audio & Video natively together for each scene flawlessly without mutating FPS metadata
        for idx, item in enumerate(timeline.get("timeline", [])):
            chunk_path = os.path.join(job_dir, f"chunk_{idx}.mp4")
            
            # Simple direct byte-mux: clamp to audio duration to guarantee sync
            audio_dur = item.get("duration", None)
            mux_cmd = [
                ffmpeg_exe,
                "-y",
                "-i", item["video_path"],
                "-i", item["audio_path"],
                "-c:v", "copy",
                "-c:a", "aac",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",  # hard-clip to whichever stream ends first
            ]
            if audio_dur:
                mux_cmd += ["-t", str(float(audio_dur))]
            mux_cmd.append(chunk_path)
            
            subprocess.run(mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            chunk_files.append(chunk_path)

        if not chunk_files:
            raise ValueError("No valid clips were parsed out of the timeline.")
            
        # Phase 2: Create strict Concat Demuxer manifest
        with open(concat_file, "w") as f:
            for c in chunk_files:
                # ffmpeg requires forward slashes securely
                safe_path = os.path.abspath(c).replace("\\", "/")
                f.write(f"file '{safe_path}'\n")
                
        # Phase 3: Instantaneous stream-copy merge (Sub-second assembly, 0 memory footprint)
        concat_cmd = [
            ffmpeg_exe,
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_path
        ]
        
        subprocess.run(concat_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Phase 4: Local footprint cleanup
        if os.path.exists(concat_file):
            os.remove(concat_file)
        for c in chunk_files:
            if os.path.exists(c):
                os.remove(c)
                
        return output_path
        
    except subprocess.CalledProcessError as sub_e:
        logger.error(f"FFmpeg binary execution critically failed: {sub_e}")
        raise sub_e
    except Exception as e:
        logger.error(f"Failed to merge final video natively: {e}")
        raise e
