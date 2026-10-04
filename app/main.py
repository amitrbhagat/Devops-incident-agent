import logging
import uuid

from fastapi import FastAPI, Request

from app.api.health import router as health_router
from app.config import get_settings
from app.logging_config import correlation_id_var, setup_logging

settings = get_settings()
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


app = FastAPI(title=settings.app_name)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    cid = request.headers.get("X-Correlation-ID") or uuid.uuid4().hex
    token = correlation_id_var.set(cid)

    try:
        response = await call_next(request)
        logger.info("%s %s -> %s", request.method, request.url.path, response.status_code)
    finally:
        correlation_id_var.reset(token)

    response.headers["X-Correlation-ID"] = cid
    return response


app.include_router(health_router)
logger.info("app started in environment=%s dry_run=%s", settings.environment, settings.dry_run)
