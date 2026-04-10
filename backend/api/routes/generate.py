from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile, File

from db.job_store import create_job, get_job
from workers.runner import dispatch_job
from workers.tasks.long_video_task import dispatch_long_video_job
from api.deps import get_current_user

router = APIRouter()


class JobCreate(BaseModel):
    topic: str
    pdf_url: Optional[str] = None


@router.post("/ppt")
async def generate_ppt(job_in: JobCreate, current_user: dict = Depends(get_current_user)):
    job_id = create_job(current_user["id"], "ppt", job_in.topic)
    dispatch_job(job_id, "ppt", job_in.topic, job_in.pdf_url)
    return {"job_id": job_id, "status": "queued"}


@router.post("/podcast")
async def generate_podcast(job_in: JobCreate, current_user: dict = Depends(get_current_user)):
    job_id = create_job(current_user["id"], "podcast", job_in.topic)
    dispatch_job(job_id, "podcast", job_in.topic, job_in.pdf_url)
    return {"job_id": job_id, "status": "queued"}

@router.post("/video")
async def generate_video(job_in: JobCreate, current_user: dict = Depends(get_current_user)):
    job_id = create_job(current_user["id"], "video", job_in.topic)
    dispatch_long_video_job(job_id, job_in.topic, job_in.pdf_url)
    return {"job_id": job_id, "status": "queued"}


@router.post("/upload-pdf")
async def upload_pdf(pdf: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    # Establish local unified storage persistence
    import os
    import shutil
    
    upload_dir = "storage/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = f"{upload_dir}/{pdf.filename}"
    
    # Save physical raw buffer 
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(pdf.file, buffer)
        
    return {"pdf_url": file_path, "status": "complete"}
