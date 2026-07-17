from typing import Any, Literal

from pydantic import BaseModel, Field

JobStatus = Literal["pending", "running", "done", "failed"]


class JobCreate(BaseModel):
    payload: dict[str, Any]
    priority: int = Field(default=0, ge=0)


class JobOut(BaseModel):
    id: str
    payload: dict[str, Any]
    status: JobStatus
    priority: int
    created_at: str
    updated_at: str
