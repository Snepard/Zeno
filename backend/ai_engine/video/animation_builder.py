import logging
from moviepy.editor import ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap

logger = logging.getLogger(__name__)

def create_scene_animation(scene: dict, output_path: str, duration: int) -> str:
    """Builds an MP4 using Pillow frames, flawlessly bypassing ImageMagick dependency!"""
    try:
        w, h = 1920, 1080
        # Build base Pillow image natively
        img = Image.new("RGB", (w, h), color=(17, 17, 22))
        draw = ImageDraw.Draw(img)
        
        # Load default font for Windows without crashing if not found
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 70)
            font_bullets = ImageFont.truetype("arial.ttf", 45)
        except OSError:
            font_title = ImageFont.load_default()
            font_bullets = ImageFont.load_default()

        # Render Heading
        heading = scene.get("heading", "")
        if heading:
            draw.text((150, 150), heading, fill="white", font=font_title)

        # Render Bullets
        bullets = scene.get("bullets", [])
        if bullets:
            bullet_y = 350
            for b in bullets:
                # Dynamically wrap text preventing it from disappearing off the edge of the canvas!
                wrapped_bullet = textwrap.fill(f"• {b}", width=60)
                draw.text((150, bullet_y), wrapped_bullet, fill=(200, 200, 210), font=font_bullets)
                # Calculate the Y offset mathematically based on lines rendered
                bullet_y += (wrapped_bullet.count('\n') + 1) * 70 + 30

        # Convert to numpy array safely
        img_np = np.array(img)
        
        # Pass native array straight to MoviePy pipeline natively mapping it to the duration
        clip = ImageClip(img_np).set_duration(duration)
        clip.fps = 24
        
        clip.write_videofile(
            output_path, 
            fps=24, 
            codec="libx264", 
            audio_codec="aac",
            preset="ultrafast",
            logger=None
        )
        clip.close()
        return output_path
    except Exception as e:
        logger.error(f"Failed to create PIL-based animation for scene: {e}")
        raise e
