import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/zeno")
client = MongoClient(MONGODB_URI)
db = client.get_default_database()
jobs = db["jobs"]


def update_job(job_id: str, status: str, output_patch=None, error: str | None = None) -> None:
    patch = {
        "status": status,
        "updatedAt": datetime.utcnow(),
    }
    if output_patch:
        patch.update({f"output.{k}": v for k, v in output_patch.items()})
    if error:
        patch["error"] = error

    jobs.update_one({"jobId": job_id}, {"$set": patch})


def mark_component_done(job_id: str, component: str) -> None:
    jobs.update_one(
        {"jobId": job_id},
        {
            "$set": {
                f"output.components.{component}": True,
                "updatedAt": datetime.utcnow(),
            }
        },
    )

    job = jobs.find_one({"jobId": job_id}, {"type": 1, "output.components": 1})
    if not job:
        return

    components = job.get("output", {}).get("components", {})
    job_type = job.get("type")

    if job_type == "lecture":
        if components.get("audio_done") and components.get("ppt_done"):
            jobs.update_one(
                {"jobId": job_id},
                {"$set": {"status": "complete", "updatedAt": datetime.utcnow()}},
            )

    if job_type == "podcast":
        if components.get("audio_done"):
            jobs.update_one(
                {"jobId": job_id},
                {"$set": {"status": "complete", "updatedAt": datetime.utcnow()}},
            )
