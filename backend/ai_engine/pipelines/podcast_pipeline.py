from ai_engine.llm.groq_client import generate_json_from_groq
from ai_engine.llm.prompts import PODCAST_SYSTEM_PROMPT
from ai_engine.chunking.script_chunker import chunk_podcast_script
from storage.local_storage import save_json
from pydantic import BaseModel, ValidationError
import logging

logger = logging.getLogger(__name__)

class DialogueLine(BaseModel):
    speaker: str
    text: str

class PodcastOutput(BaseModel):
    topic: str
    dialogue: list[DialogueLine]

def run_podcast_pipeline(job_id: str, topic: str):
    logger.info(f"Executing Groq-powered Podcast dialogue pipeline sequence mapping inside job {job_id}")
    
    user_prompt = f"Create a podcast script exploring natively mapping core components targeting topic: '{topic}'"
    raw_json = generate_json_from_groq(PODCAST_SYSTEM_PROMPT, user_prompt, temperature=0.3)
    
    try:
        validated = PodcastOutput(**raw_json)
        script_data = validated.model_dump()
    except ValidationError as e:
        logger.error(f"Pydantic execution strict schemas explicitly denied formatting outputs: {e}")
        raise ValueError(f"Groq mapping fully faulted on internal schema parsing: {e}")

    script_path = save_json(job_id, "script.json", script_data)
    
    chunks = chunk_podcast_script(script_data)
    chunks_path = save_json(job_id, "chunks.json", chunks)
    
    return {
        "script": script_data,
        "paths": {
            "script": script_path,
            "chunks": chunks_path
        }
    }
