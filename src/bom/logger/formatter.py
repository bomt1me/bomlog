import datetime
import inspect
import json
import logging
import traceback
from typing import Any, Dict


RESERVED_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


EASY_TYPES = (str, bool, dict, float, int, list, type(None))


def basic_type_encoder(obj: Any) -> Any:
    if isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
        return obj.isoformat()

    if inspect.istraceback(obj):
        return "".join(traceback.format_tb(obj)).strip()

    if isinstance(obj, (Exception, type)):
        return str(obj)

    try:
        return str(obj)
    except Exception:  # pylint: disable=broad-except
        return None


def get_extra_fields(record: logging.LogRecord) -> Dict[str, Any]:
    fields = {}
    for key, value in record.__dict__.items():
        if key not in RESERVED_ATTRS:
            if isinstance(value, EASY_TYPES):
                fields[key] = value
            else:
                fields[key] = basic_type_encoder(value)
    return fields


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        dict_message = {
            "asctime": self.formatTime(record, self.datefmt),
            "created": record.created,
            "exc_info": record.exc_info,
            "filename": record.filename,
            "funcName": record.funcName,
            "levelname": record.levelname,
            "levelno": record.levelno,
            "lineno": record.lineno,
            "module": record.module,
            "msecs": record.msecs,
            "name": record.name,
            "pathname": record.pathname,
            "process": record.process,
            "processName": record.processName,
            "relativeCreated": record.relativeCreated,
            "thread": record.thread,
            "threadName": record.threadName,
        }

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if not record.stack_info:
            record.stack_info = ""

        dict_message.update(
            {
                "exc_text": record.exc_text,
                "stack_info": self.formatStack(record.stack_info),
                "msg": record.getMessage(),
            }
        )

        dict_message.update(get_extra_fields(record))
        return json.dumps(dict_message)
