import json
import sys
import logging
from contextvars import ContextVar
from datetime import datetime, timezone


correlation_id_var : ContextVar[str] = ContextVar("correlation_id", default="-")


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz = timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id_var.get()
        }
        if record.exc_info:
            payload["exeption"] = self.formatException(record.exc_info)
        return json.dumps(payload)



def setup_logging(level: str = "INFO") -> str:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level) 

    for name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        lg = logging.getLogger(name)
        lg.handlers = []
        lg.propagate = True
