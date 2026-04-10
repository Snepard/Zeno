from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from db.job_store import create_job, get_job
from workers.runner import dispatch_job
from api.deps import get_current_user

router = APIRouter()


class JobCreate(BaseModel):
    topic: str


@router.post("/ppt")
async def generate_ppt(job_in: JobCreate, current_user: dict = Depends(get_current_user)):
    job_id = create_job(current_user["id"], "ppt", job_in.topic)
    dispatch_job(job_id, "ppt", job_in.topic)
    return {"job_id": job_id, "status": "queued"}


@router.post("/podcast")
async def generate_podcast(job_in: JobCreate, current_user: dict = Depends(get_current_user)):
    job_id = create_job(current_user["id"], "podcast", job_in.topic)
    dispatch_job(job_id, "podcast", job_in.topic)
    return {"job_id": job_id, "status": "queued"}
