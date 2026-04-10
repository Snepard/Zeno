from ai_engine.llm.groq_client import generate_class_completion
from ai_engine.llm.prompts import PPT_SYSTEM_PROMPT
from ai_engine.chunking.script_chunker import chunk_ppt_script
from storage.local_storage import save_json
from pydantic import BaseModel, ValidationError
import logging

logger = logging.getLogger(__name__)

# Rapid Pydantic structured verification logic natively executing
class SlideOutput(BaseModel):
    slide_no: int
    title: str
    bullets: list[str]
    explanation: str
    keywords: list[str]

class PPTOutput(BaseModel):
    topic: str
    slides: list[SlideOutput]

def run_ppt_pipeline(job_id: str, topic: str, pdf_url: str = None):
    logger.info(f"Executing Groq-powered native LLM PPT generation pipeline inside job {job_id}")
    
    # 1. Engage Groq explicitly leveraging optimization variables correctly
    user_prompt = f"Create a detailed presentation on the core topic: '{topic}'"
    
    if pdf_url:
        try:
            import fitz 
            doc = fitz.open(pdf_url)
            context = ""
            for page in doc:
                context += page.get_text() + "\n"
            user_prompt += f"\n\nSource material context:\n{context[:2000]}"
        except Exception as e:
            logger.error(f"Failed to natively process PDF context: {e}")
    raw_json = generate_class_completion(PPT_SYSTEM_PROMPT, user_prompt, temperature=0.3)
    
    # 2. Re-Validate fully through Pydantic ensuring downstream safety
    try:
        validated = PPTOutput(**raw_json)
        script_data = validated.model_dump()
    except ValidationError as e:
        logger.error(f"Live Pydantic structure strictly disallowed execution schemas formatting: {e}")
        raise ValueError(f"Groq rendered fundamentally problematic JSON layouts natively bypassing heuristics: {e}")

    # 3. Store Script robustly inside independent metadata wrappers
    script_path = save_json(job_id, "script.json", script_data)
    
    # 4. Synthesize structural groupings formatting Vector native chunk strings globally
    chunks = chunk_ppt_script(script_data)
    chunks_path = save_json(job_id, "chunks.json", chunks)
    
    # NEW STEP: FAISS Vector RAG index compilation triggered seamlessly locally
    from ai_engine.rag.vector_store import build_and_save_index
    try:
        build_and_save_index(job_id, chunks)
    except Exception as ve:
        logger.error(f"[RAG FAISS ERROR] Extracted chunks failed compiling: {ve}")
    
    # 5. Return explicit memory references
    return {
        "script": script_data,
        "paths": {
            "script": script_path,
            "chunks": chunks_path
        }
    }
