"""
JSON-based Job Store — replaces PostgreSQL entirely.
All job state is persisted to storage/jobs.json as a flat dictionary.
Thread-safe via a simple file lock pattern (no concurrent writes race).
"""
import json
import uuid
import threading
from pathlib import Path
from datetime import datetime

STORAGE_DIR = Path("storage")
STORAGE_DIR.mkdir(exist_ok=True)
JOBS_FILE = STORAGE_DIR / "jobs.json"

_lock = threading.Lock()


def _load() -> dict:
    if not JOBS_FILE.exists():
        return {}
    with open(JOBS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save(jobs: dict):
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, default=str)


def create_job(user_id: str, job_type: str, topic: str) -> str:
    job_id = str(uuid.uuid4())
    with _lock:
        jobs = _load()
        jobs[job_id] = {
            "job_id": job_id,
            "user_id": user_id,
            "type": job_type,
            "topic": topic,
            "status": "queued",
            "progress": 0,
            "result": None,
            "error": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        _save(jobs)
    return job_id


def get_job(job_id: str) -> dict | None:
    with _lock:
        jobs = _load()
    return jobs.get(job_id)


def update_job(job_id: str, status: str = None, progress: int = None,
               result: dict = None, error: str = None):
    with _lock:
        jobs = _load()
        job = jobs.get(job_id)
        if not job:
            return
        if status is not None:
            job["status"] = status
        if progress is not None:
            job["progress"] = progress
        if result is not None:
            existing = job.get("result") or {}
            if isinstance(existing, dict) and isinstance(result, dict):
                existing.update(result)
                job["result"] = existing
            else:
                job["result"] = result
        if error is not None:
            job["error"] = error
        job["updated_at"] = datetime.utcnow().isoformat()
        jobs[job_id] = job
        _save(jobs)
