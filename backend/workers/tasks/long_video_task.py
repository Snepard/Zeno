import logging
import threading
import json
from pathlib import Path
from db.job_store import update_job
from ai_engine.video.long_video_pipeline import process_pdf_to_script
from ai_engine.video.scene_generator import generate_scenes_from_script
from ai_engine.tts.tts_manager import generate_audio_manager
from ai_engine.video.minim_renderer import render_scene_with_minim
from ai_engine.video.animation_builder import create_scene_animation
from ai_engine.video.timeline_manager import build_timeline, get_audio_duration
from ai_engine.video.video_merger import merge_timeline

logger = logging.getLogger(__name__)

def _run_long_video_task(job_id: str, topic: str, pdf_url: str = None):
    """
    Robust native runner task strictly bypassing pure blocking behavior.
    Step 1: PDF -> Script (25%)
    Step 2: Scenes (40%)
    Step 3: TTS & Render (85%)
    Step 4: Merge (100%)
    """
    try:
        job_dir_str = f"storage/{job_id}"
        job_dir = Path(job_dir_str)
        job_dir.mkdir(parents=True, exist_ok=True)
        (job_dir / "scenes").mkdir(exist_ok=True)
        (job_dir / "audio").mkdir(exist_ok=True)
        
        # 1. Pipeline: PDF -> Transcript Script
        update_job(job_id, status="processing", progress=10)
        script_data = process_pdf_to_script(pdf_url, topic)
        
        # Write to script.json internally for continuity
        with open(job_dir / "script.json", "w", encoding="utf-8") as f:
            json.dump(script_data, f, indent=2)
            
        update_job(job_id, progress=25, result={"topic": topic, "script": script_data})
        
        # 2. Pipeline: Generate Scenes
        sections = script_data.get("sections", [])
        scenes_data = generate_scenes_from_script(sections)
        scenes = scenes_data.get("scenes", [])
        
        update_job(job_id, progress=40)
        
        # 3. Pipeline: Generate Assets (audio-first, then render to exact audio duration)
        total_scenes = len(scenes)
        for idx, scene in enumerate(scenes):
            try:
                scene_id = scene.get("scene_id", idx + 1)

                # ── Step A: Generate TTS audio FIRST ──────────────────────────
                tts_text = scene.get("text", "")
                audio_filename = f"scene_{scene_id}.mp3"
                generate_audio_manager(tts_text, job_id, audio_filename)

                # ── Step B: Measure ACTUAL audio duration ──────────────────────
                audio_path = str(job_dir / "audio" / audio_filename)
                actual_duration = get_audio_duration(audio_path)
                logger.info(f"Scene {scene_id}: audio={actual_duration:.2f}s (LLM est={scene.get('duration')}s)")

                # ── Step C: Render Manim to EXACTLY match audio length ─────────
                scene_vid_path = str(job_dir / "scenes" / f"scene_{scene_id}.mp4")

                try:
                    render_scene_with_minim(scene, scene_vid_path, int(actual_duration))
                except Exception as minim_err:
                    logger.warning(f"Minim failed for scene {scene_id}: {minim_err}. Falling back to Pillow.")
                    create_scene_animation(scene, scene_vid_path, int(actual_duration))

            except Exception as se:
                logger.warning(f"Scene {scene.get('scene_id', idx)} failed encoding loop: {se}")

            cur_prog = 40 + int(((idx + 1) / total_scenes) * 45)
            update_job(job_id, progress=cur_prog)

            
        # 4. Pipeline: Timeline & Merging
        timeline_data = build_timeline(scenes, job_dir_str)
        with open(job_dir / "timeline.json", "w", encoding="utf-8") as f:
            json.dump(timeline_data, f, indent=2)
            
        update_job(job_id, progress=90)
        
        output_video = str(job_dir / "lecture.mp4")
        merge_timeline(timeline_data, output_video)
        
        # COMPLETED
        update_job(job_id, status="completed", progress=100, result={"video_url": f"/storage/{job_id}/lecture.mp4", "script": script_data})
        logger.info(f"Long-form Video {job_id} completely assembled into {output_video}")

    except Exception as e:
        logger.error(f"Long-form video task {job_id} completely failed: {e}", exc_info=True)
        update_job(job_id, status="failed", error=str(e))

def dispatch_long_video_job(job_id: str, topic: str, pdf_url: str = None):
    """Fire and forget daemon thread. Emulates Celery worker queue logic beautifully locally."""
    t = threading.Thread(target=_run_long_video_task, args=(job_id, topic, pdf_url), daemon=True)
    t.start()
    logger.info(f"Dispatched pure long video automation thread for {job_id}")
