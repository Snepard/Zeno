import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "storage"))

def ensure_job_directory(job_id: str) -> Path:
    """Ensures a directory exists for a specific job_id in the storage system."""
    job_dir = STORAGE_DIR / job_id
    if not job_dir.exists():
        job_dir.mkdir(parents=True, exist_ok=True)
    return job_dir

def save_json(job_id: str, filename: str, data: dict) -> str:
    """Saves a Python dictionary as a JSON file locally."""
    try:
        job_dir = ensure_job_directory(job_id)
        filepath = job_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return str(filepath)
    except Exception as e:
        logger.error(f"Failed to save JSON to {filename} for job {job_id}: {e}")
        raise e

def read_json(job_id: str, filename: str) -> dict:
    """Reads a JSON file from the local storage system."""
    job_dir = STORAGE_DIR / job_id
    filepath = job_dir / filename
    if not filepath.exists():
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
