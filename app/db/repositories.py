from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AuditLog, Incident


def add_audit(db:Session, *, incident_id: int | None, actor:str, event:str, details:dict | None=None) -> AuditLog:
    entry = AuditLog(incident_id=incident_id, actor=actor, event=event, details=details)
    db.add(entry)
    return entry


def create_incident(db:Session, *, fingerprint: str, service:str, namespace:str, severity:str, summary:str | None=None) -> Incident:
    incident = Incident(
        fingerprint=fingerprint,
        service=service,
        namespace=namespace,
        severity=severity,
        summary=summary,
    )    
    db.add(incident)
    db.flush()
    add_audit(
        db,
        incident_id=incident.id,
        actor="system",
        event="incident_created",
        details={"service":service, "severity":severity},
    )
    db.commit()
    db.refresh(incident)
    return incident


def get_incident(db: Session, incident_id: int) -> Incident | None:
    return db.get(Incident, incident_id)


def list_incidents(db: Session, limit: int = 50) -> list[Incident]:
    stmt = select(Incident).order_by(Incident.id.desc()).limit(limit)
    return list(db.scalars(stmt))


def list_audit_for_incident(db: Session, incident_id: int) -> list[AuditLog]:
    stmt = select(AuditLog).where(AuditLog.incident_id==incident_id).order_by(AuditLog.id)
    return list(db.scalars(stmt))
