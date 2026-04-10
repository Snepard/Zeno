import json
import logging
from ai_engine.pdf.pdf_parser import extract_text_from_pdf
from ai_engine.llm.groq_client import generate_video_completion

logger = logging.getLogger(__name__)

LONG_VIDEO_PROMPT = """You are a world-class AI educational filmmaker, physicist, and visualization expert.
Your job: DEEPLY understand the topic and produce a VISUAL-FIRST, animated breakdown — like 3Blue1Brown.

For EVERY section you must ask yourself:
  - Can this be an equation that builds up incrementally?
  - Can this be a force diagram, with arrows showing magnitude and direction?
  - Should I show an orbit or wave to demonstrate the physics?
  - Is this a transformation (one state → another)?
  - Is this a flow of steps? A neural network? A graph of data?
  - Is this a comparison of two concepts side-by-side?
  - Can I show a timeline of events?

AVAILABLE VISUAL TYPES:
- `equation`    → A mathematical equation that writes itself on screen, with step-by-step derivation below it
- `graph`       → An animated X/Y graph with data points and a curve
- `orbit`       → Planets / electrons / celestial bodies orbiting a central body (gravity, electrons, etc.)
- `wave`        → An animated sine/cosine/signal wave (sound, light, oscillation)
- `force`       → Arrows showing forces acting on an object (physics diagrams)
- `transform`   → One concept morphing/transforming into another shape-by-shape
- `flow`        → A flowchart of steps/decisions building top to bottom
- `neural`      → Animated neural network with signal propagation (AI, brain, networks)
- `comparison`  → Two concepts side-by-side with labels (Classical vs Quantum, etc.)
- `timeline`    → A horizontal sequence of events/epochs
- `diagram`     → A node-graph showing relationships between entities
- `code`        → A syntax-highlighted code block building line by line
- `bullet`      → LAST RESORT ONLY if none of the above fits

OUTPUT ONLY valid JSON:
{
  "topic": "string",
  "sections": [
    {
      "title": "Section Title",
      "explanation": "Detailed engaging narrator script for this section.",
      "duration_estimate": 25,
      "visual_concept": {
        "type": "<one of the types above>",
        "description": "Exact description: what appears on screen, what moves, what is labeled.",
        "equation": "LaTeX string e.g. F = ma or E = \\frac{1}{2}mv^2",
        "steps": ["Step 1", "Step 2", "Step 3"],
        "elements": ["Node A", "Node B"],
        "labels": ["Label A", "Label B"],
        "relationships": [["A", "B"], ["B", "C"]],
        "x_axis": "Time (s)",
        "y_axis": "Velocity (m/s)",
        "data_points": [[0,0],[1,2],[2,4],[3,3]],
        "left_items": ["Classical: deterministic"],
        "right_items": ["Quantum: probabilistic"]
      }
    }
  ]
}

RULES:
- `bullet` is FORBIDDEN unless the concept is genuinely a list with no visual metaphor.
- Every `equation` MUST include the actual LaTeX string.
- Every `graph` MUST include data_points.
- Every `orbit` MUST include labels (what is orbiting what).
- Every `comparison` MUST include left_items and right_items.
- Output ONLY valid JSON. No markdown, no extra text.
"""

def process_pdf_to_script(pdf_url: str = None, topic: str = None) -> dict:
    """Entry point for parsing the input into a dynamic script."""
    text_context = ""
    if pdf_url:
        text_context = extract_text_from_pdf(pdf_url)
    
    prompt_payload = f"Topic: {topic}\n\nContext:\n{text_context}"
    completion = generate_video_completion(
        user_prompt=prompt_payload,
        system_prompt=LONG_VIDEO_PROMPT
    )
    return completion or {"topic": topic, "sections": []}
