import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler

_SECONDS_PER_DAY = 86400


class _SizedTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Rotate the log daily and whenever it exceeds ``max_bytes``.

    Retention is enforced by age: any rotated file older than ``backup_count``
    days is removed on the next rollover, so the directory keeps at most that
    many days of history regardless of how often size-based rotation fires.
    """

    def __init__(self, filename: str, max_bytes: int, backup_count: int) -> None:
        super().__init__(
            filename,
            when="midnight",
            backupCount=backup_count,
            encoding="utf-8",
            utc=True,
        )
        self.max_bytes = max_bytes

    def shouldRollover(self, record: logging.LogRecord) -> bool:
        if self.max_bytes > 0 and self.stream is not None:
            self.stream.seek(0, 2)
            position = self.stream.tell()
            # Roll over *before* writing a record that would push the file past
            # the cap, so each segment stays within max_bytes. Never rotate an
            # empty file, otherwise a single record larger than the cap would
            # spin off endless empty segments.
            if position > 0:
                message = self.format(record) + self.terminator
                encoded = len(message.encode(self.encoding or "utf-8"))
                if position + encoded >= self.max_bytes:
                    return True
        return bool(super().shouldRollover(record))

    def rotation_filename(self, default_name: str) -> str:
        # Several size-based rollovers can happen within the same day and would
        # otherwise resolve to the same dated filename; append a counter so an
        # earlier segment is never overwritten.
        if not os.path.exists(default_name):
            return default_name
        index = 1
        while os.path.exists(f"{default_name}.{index}"):
            index += 1
        return f"{default_name}.{index}"

    def getFilesToDelete(self) -> list[str]:
        # Age-based retention: delete every rotated file last modified more than
        # ``backupCount`` days ago. This also reaps the counter-suffixed files
        # produced by same-day size rollovers, which the stock suffix matcher
        # would skip.
        if self.backupCount <= 0:
            return []
        dir_name, base_name = os.path.split(self.baseFilename)
        prefix = base_name + "."
        cutoff = time.time() - self.backupCount * _SECONDS_PER_DAY
        stale: list[str] = []
        try:
            names = os.listdir(dir_name)
        except FileNotFoundError:
            # The log directory was removed out from under us (e.g. an external
            # cleanup between rollovers). Nothing to reap; the next emit will
            # recreate the directory and base file.
            return []
        for name in names:
            if not name.startswith(prefix):
                continue
            path = os.path.join(dir_name, name)
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                # The file vanished between listing and stat; skip it.
                continue
            if mtime < cutoff:
                stale.append(path)
        return stale


def configure_logging(
    log_dir: str,
    log_retention_days: int,
    log_max_bytes: int,
    log_level: int | str = logging.INFO,
) -> None:
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "app.log")

    root = logging.getLogger()
    root.setLevel(log_level)

    if not root.handlers:
        root.addHandler(logging.StreamHandler())

    # Re-creating the app (tests, reload) must not stack duplicate file handlers
    # on the same path, which would multiply writes and break rotation renames.
    if _has_file_handler(root, log_path):
        return

    handler = _SizedTimedRotatingFileHandler(
        filename=log_path,
        max_bytes=log_max_bytes,
        backup_count=log_retention_days,
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    root.addHandler(handler)


def _has_file_handler(logger: logging.Logger, log_path: str) -> bool:
    target = os.path.abspath(log_path)
    return any(
        isinstance(handler, _SizedTimedRotatingFileHandler)
        and os.path.abspath(handler.baseFilename) == target
        for handler in logger.handlers
    )
