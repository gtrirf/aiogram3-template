import logging
import sys
from datetime import datetime
from pathlib import Path

from app.config import settings


class TZFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=settings.tz)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime("%Y-%m-%d %H:%M:%S")


def setup_logging(level=logging.INFO):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Handlers
    console_handler = logging.StreamHandler(sys.stdout)

    file_handler = logging.FileHandler(logs_dir / "bot.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    error_file_handler = logging.FileHandler(logs_dir / "error.log", encoding="utf-8")
    error_file_handler.setLevel(logging.ERROR)

    formatter = TZFormatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s:%(lineno)d - %(message)s",
    )

    for h in (console_handler, file_handler, error_file_handler):
        h.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()

    root.addHandler(console_handler)
    root.addHandler(file_handler)
    root.addHandler(error_file_handler)