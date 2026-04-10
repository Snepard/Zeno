from fastapi import APIRouter, Depends, HTTPException
from api.deps import get_current_user
from db.job_store import get_job

router = APIRouter()


@router.get("/{job_id}")
async def get_job_status(job_id: str, current_user: dict = Depends(get_current_user)):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
