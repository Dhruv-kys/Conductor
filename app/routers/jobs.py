import json
import time
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.redis_client import redis_client
from app.schemas import JobCreate, JobOut, JobStatus

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _job_key(job_id: str) -> str:
    return f"job:{job_id}"


def _hash_to_job(data: dict) -> JobOut:
    return JobOut(
        id=data["id"],
        payload=json.loads(data["payload"]),
        status=data["status"],
        priority=int(data["priority"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


@router.post("", response_model=JobOut, status_code=201)
def create_job(job: JobCreate) -> JobOut:
    job_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    fields = {
        "id": job_id,
        "payload": json.dumps(job.payload),
        "status": "pending",
        "priority": job.priority,
        "created_at": now,
        "updated_at": now,
    }

    pipe = redis_client.pipeline()
    pipe.hset(_job_key(job_id), mapping=fields)
    pipe.zadd("jobs:pending", {job_id: job.priority})
    pipe.zadd("jobs:all", {job_id: time.time()})
    pipe.execute()

    return JobOut(
        id=job_id,
        payload=job.payload,
        status="pending",
        priority=job.priority,
        created_at=now,
        updated_at=now,
    )


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: str) -> JobOut:
    data = redis_client.hgetall(_job_key(job_id))

    if not data:
        raise HTTPException(status_code=404, detail="job not found")

    return _hash_to_job(data)


@router.get("", response_model=list[JobOut])
def list_jobs(status: JobStatus | None = None) -> list[JobOut]:
    job_ids = redis_client.zrevrange("jobs:all", 0, -1)

    jobs = []
    for job_id in job_ids:
        data = redis_client.hgetall(_job_key(job_id))
        if not data:
            continue
        job = _hash_to_job(data)
        if status is None or job.status == status:
            jobs.append(job)

    return jobs
