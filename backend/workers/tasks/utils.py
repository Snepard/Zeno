# Thin shim so old imports like `from workers.tasks.utils import sync_update_job` still work
from db.job_store import update_job


def sync_update_job(job_id: str, status=None, progress: int = None,
                    result: dict = None, error: str = None):
    """Backward-compatible wrapper around the JSON job store."""
    status_val = status.value if hasattr(status, "value") else status
    update_job(job_id, status=status_val, progress=progress, result=result, error=error)
