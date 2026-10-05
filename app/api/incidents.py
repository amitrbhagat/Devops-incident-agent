from datetime import datetime
from typing import Literal

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.db import repositories as repo
from app.db.session import DbSession


router = APIRouter(prefix="/incidents", tags=["incidents"])


class IncidentCreate(BaseModel):
    fingerprint: str = Field(min_length=1, max_length=64)
    service: str = Field(min_length=1, max_length=100)
    namespace: str = Field(min_length=1, max_length=100)
    severity: Literal["info", "warning", "critical"]
    summary: str | None = None


class IncidentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fingerprint: int
    service: str
    namespace: str
    severity: str
    status: str
    summary: str
    started_at: datetime
    resolved_at: datetime | None


@router.post("", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
def create_incident(body:IncidentCreate, db:DbSession):
    return repo.create_incident(db, **body.model_dump())


@router.get("", response_model=list[IncidentOut])
def list_incidents(db: DbSession, limit: int=50):
    return repo.list_incidents(db, limit=min(limit, 200))


@router.get("/{incident_id}", repsonse_model=IncidentOut)
def get_incident(incident_id: int, db: DbSession):
    incident = repo.get_incident(db, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="incident not found")
    return incident
