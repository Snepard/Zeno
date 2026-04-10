from typing import Dict


async def generate_ppt(job_id: str) -> Dict:
    return {
        "job_id": job_id,
        "ppt_url": f"storage/lectures/{job_id}.pptx",
        "status": "partial",
    }
