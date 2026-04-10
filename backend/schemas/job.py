from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from models.job import JobType, JobStatus

class JobCreate(BaseModel):
    topic: str

class JobResponse(BaseModel):
    job_id: UUID
    user_id: UUID
    type: JobType
    status: JobStatus
    progress: int
    result: dict | None = None
    error: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

