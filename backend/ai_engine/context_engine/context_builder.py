from ai_engine.rag.retriever import retrieve_context
from ai_engine.memory.memory_store import get_user_memory
from storage.local_storage import ensure_job_directory
import json
import logging

logger = logging.getLogger(__name__)

def build_context(job_id: str, user_id: str, current_slide: int, question: str, mode: str):
    """
    Massively core execution layer uniting: RAG Vectors + Static Structurals + Chat memory.
    Dynamically routes logic parsing based natively upon exact module intents natively.
    """
    job_dir = ensure_job_directory(job_id)
    script_path = job_dir / "script.json"
    
    script_data = {}
    if script_path.exists():
        with open(script_path, "r") as f:
            script_data = json.load(f)
            
    # Universal execution route overriding vectors aggressively covering entire documents
    if mode == "summarize":
        return {
            "relevant_chunks": [script_data], 
            "current_slide_data": {}, 
            "history": [], 
            "mode": mode
        }
        
    # Poll FAISS Vector natively checking related elements efficiently.
    relevant_chunks = retrieve_context(job_id, question, top_k=3)
    history = get_user_memory(job_id, user_id, top_n=3)
    
    current_slide_data = {}
    if current_slide is not None:
        if "slides" in script_data:
            for slide in script_data["slides"]:
                if slide.get("slide_no") == int(current_slide):
                    current_slide_data = slide
                    break
        elif "dialogue" in script_data:
             # Support podcast indexing logically mapping turn chunks natively
             items = script_data.get("dialogue", [])
             if 0 <= current_slide < len(items):
                 current_slide_data = items[current_slide]
                
    return {
        "relevant_chunks": relevant_chunks,
        "current_slide_data": current_slide_data,
        "history": history,
        "mode": mode
    }
