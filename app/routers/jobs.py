import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.db import get_db
from app.schemas import JobCreate, JobOut, JobStatus

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _row_to_job(row) -> JobOut:
    return JobOut(
        id=row["id"],
        payload=json.loads(row["payload"]),
        status=row["status"],
        priority=row["priority"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


@router.post("", response_model=JobOut, status_code=201)
def create_job(job: JobCreate) -> JobOut:
    job_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO jobs (id, payload, status, priority, created_at, updated_at)
            VALUES (?, ?, 'pending', ?, ?, ?)
            """,
            (job_id, json.dumps(job.payload), job.priority, now, now),
        )

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
    with get_db() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="job not found")

    return _row_to_job(row)


@router.get("", response_model=list[JobOut])
def list_jobs(status: JobStatus | None = None) -> list[JobOut]:
    with get_db() as conn:
        if status is not None:
            rows = conn.execute(
                "SELECT * FROM jobs WHERE status = ? ORDER BY created_at DESC", (status,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()

    return [_row_to_job(row) for row in rows]
