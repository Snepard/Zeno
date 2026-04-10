import json
from pathlib import Path
from storage.local_storage import ensure_job_directory
import logging

logger = logging.getLogger(__name__)

def get_user_memory(job_id: str, user_id: str, top_n: int = 5) -> list:
    """Safely maps previous conversation turns specific to exact users across specific modules locally."""
    job_dir = ensure_job_directory(job_id)
    mem_path = job_dir / f"memory_{user_id}.json"
    
    if not mem_path.exists():
        return []
        
    try:
        with open(mem_path, "r") as f:
            data = json.load(f)
        return data[-top_n:]
    except Exception as e:
        logger.warning(f"Failed to fetch conversation history {job_id} / {user_id}: {e}")
        return []

def add_user_memory(job_id: str, user_id: str, question: str, answer: str):
    """Dynamically extends conversation memory strictly retaining context seamlessly."""
    job_dir = ensure_job_directory(job_id)
    mem_path = job_dir / f"memory_{user_id}.json"
    
    data = []
    if mem_path.exists():
        try:
            with open(mem_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            pass # Reset memory natively
            
    data.append({
        "question": question,
        "answer": answer
    })
    
    with open(mem_path, "w") as f:
        json.dump(data, f, indent=2)
