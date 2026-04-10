import json
import re
import logging

logger = logging.getLogger(__name__)

def clean_json_string(raw_text: str) -> str:
    """Attempts to clean corrupted JSON strings by stripping stray syntax formatting."""
    # Remove markdown code block fences if present erroneously
    cleaned = re.sub(r'```json\s*', '', raw_text)
    cleaned = re.sub(r'```\s*', '', cleaned)
    
    # Remove leading/trailing blank spaces
    cleaned = cleaned.strip()
    
    # Automatically heal invalid trailing commas immediately before structurally closing braces
    cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
    
    return cleaned

def parse_llm_json(raw_text: str) -> dict:
    """
    Safely parses JSON outputs from Groq LLMs. Attempting programmatic healing of broken syntax 
    prior to structurally defaulting.
    Raises ValueError safely catching downstream layers securely.
    """
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        logger.warning(f"Invalid structural JSON detected. Engaging active heuristics engine...")
        
        # Secondary fallback structural heuristic patching
        cleaned_text = clean_json_string(raw_text)
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError as final_err:
            logger.error(f"Heuristics bypassed. Final parse completely ruined on structure. Snippet: {raw_text[:50]}")
            raise ValueError(f"LLM JSON parsing completely halted. Groq failed schema parameters: {final_err}")
