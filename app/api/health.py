import logging 

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.config import get_settings
from app.db.session import DbSession

router = APIRouter()
logger = logging.getlogger(__name__)


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/ready")
def ready(db: DbSession) -> dict:
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        logger.exception("readiness check failed: database unreachable")
        raise HTTPException(status_code=503, detail="database unavailable") from None
    return {"status": "ready", "environment": get_settings().environment}
