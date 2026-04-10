import logging
from ai_engine.llm.groq_client import generate_video_completion

logger = logging.getLogger(__name__)

SCENE_PROMPT = """You are an expert Manim animation director.
You receive a structured educational script where each section has a `visual_concept` that describes what should be animated.

Your job is to translate each section into a precise scene JSON object for the Manim rendering engine.

REQUIRED OUTPUT FORMAT:
{
  "scenes": [
    {
      "scene_id": 1,
      "text": "Full spoken narration in PLAIN ENGLISH. No LaTeX, no symbols like ^2 or \\\\frac. Write it so Edge TTS can read it naturally.",
      "heading": "Short title shown on screen",
      "visual_type": "graph | equation | flow | diagram | timeline | comparison | neural | code | orbit | wave | force | transform | bullet",
      "duration": 25,
      "equation": "LaTeX string e.g. F = ma",
      "steps": ["F = Force — the push or pull on the object", "m = Mass — how heavy the object is", "a = Acceleration — how fast velocity changes"],
      "elements": ["Node A", "Node B", "Node C"],
      "labels": ["Input Layer", "Hidden Layer", "Output Layer"],
      "relationships": [["Node A", "Node B"], ["Node B", "Node C"]],
      "data_points": [[0,0],[1,2],[2,1],[3,4]],
      "x_axis": "Time (seconds)",
      "y_axis": "Velocity (m/s)",
      "left_items": ["Classical Bit: 0 or 1"],
      "right_items": ["Qubit: 0, 1, or both"],
      "bullets": ["Only if type=bullet: key point 1", "key point 2"]
    }
  ]
}

RULES:
- `text` is the SPOKEN audio script. Write ONLY natural English. Never put LaTeX, \\frac, ^2, or symbols in `text`.
- For `visual_type=equation`, the `steps` field MUST be a list of 'SYMBOL = Plain English meaning' strings.
  Example: ["E = Total Energy of the object", "m = Mass of the object", "c = Speed of light (300 million m/s)"]
- Match `visual_type` EXACTLY from the input `visual_concept.type`.
- `duration` must be realistic (15-45 seconds per scene).
- Output ONLY valid JSON. No markdown, no extra text.
"""


def generate_scenes_from_script(script_sections: list) -> dict:
    """Translates deep script sections with visual concepts into precise Manim scene directives."""
    import json
    sections_payload = json.dumps(script_sections, indent=2)
    completion = generate_video_completion(
        user_prompt=f"Script Sections:\n{sections_payload}",
        system_prompt=SCENE_PROMPT
    )
    return completion or {"scenes": []}
