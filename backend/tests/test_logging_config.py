import logging
import os
import shutil
import time

from app.core.logging_config import (
    _SizedTimedRotatingFileHandler,
    configure_logging,
)


def _rotated_files(log_dir: str) -> list[str]:
    return sorted(
        name
        for name in os.listdir(log_dir)
        if name.startswith("app.log.")
    )


def test_size_rollovers_within_a_day_do_not_overwrite_each_other(tmp_path) -> None:
    log_path = os.path.join(tmp_path, "app.log")
    handler = _SizedTimedRotatingFileHandler(log_path, max_bytes=1, backup_count=3)
    logger = logging.getLogger("test_size_rollover")
    logger.handlers = [handler]
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    try:
        # max_bytes=1 forces a rollover on every emit after the first.
        for _ in range(5):
            logger.info("x" * 100)
    finally:
        handler.close()

    rotated = _rotated_files(tmp_path)
    # 5 emits -> 4 rollovers -> 4 distinct rotated segments, none overwritten.
    assert len(rotated) == 4
    assert len(set(rotated)) == 4


def test_each_segment_stays_within_the_size_cap(tmp_path) -> None:
    log_path = os.path.join(tmp_path, "app.log")
    max_bytes = 2000
    handler = _SizedTimedRotatingFileHandler(log_path, max_bytes=max_bytes, backup_count=3)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger = logging.getLogger("test_size_cap")
    logger.handlers = [handler]
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    try:
        for i in range(300):
            logger.info("event %04d %s", i, "y" * 80)
    finally:
        handler.close()

    for name in os.listdir(tmp_path):
        if name == "app.log" or name.startswith("app.log."):
            assert os.path.getsize(os.path.join(tmp_path, name)) <= max_bytes


def test_retention_deletes_files_older_than_backup_count_days(tmp_path) -> None:
    log_path = os.path.join(tmp_path, "app.log")

    stale = os.path.join(tmp_path, "app.log.2000-01-01")
    fresh = os.path.join(tmp_path, "app.log.2999-01-01")
    for path in (stale, fresh):
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("old\n")
    ten_days_ago = time.time() - 10 * 86400
    os.utime(stale, (ten_days_ago, ten_days_ago))

    handler = _SizedTimedRotatingFileHandler(log_path, max_bytes=1, backup_count=3)
    logger = logging.getLogger("test_retention")
    logger.handlers = [handler]
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    try:
        # Two emits guarantee at least one rollover, which triggers cleanup.
        logger.info("first")
        logger.info("second")
    finally:
        handler.close()

    assert not os.path.exists(stale)
    assert os.path.exists(fresh)


def test_get_files_to_delete_tolerates_missing_log_dir(tmp_path) -> None:
    log_dir = os.path.join(tmp_path, "logs")
    os.makedirs(log_dir)
    log_path = os.path.join(log_dir, "app.log")
    handler = _SizedTimedRotatingFileHandler(log_path, max_bytes=1, backup_count=3)

    try:
        # Simulate the directory being removed out from under the handler
        # between rollovers; cleanup must not raise.
        handler.close()
        shutil.rmtree(log_dir)
        assert handler.getFilesToDelete() == []
    finally:
        handler.close()


def test_configure_logging_is_idempotent(tmp_path) -> None:
    root = logging.getLogger()
    original = list(root.handlers)
    try:
        root.handlers = []
        configure_logging(str(tmp_path), log_retention_days=3, log_max_bytes=1024)
        configure_logging(str(tmp_path), log_retention_days=3, log_max_bytes=1024)

        file_handlers = [
            handler
            for handler in root.handlers
            if isinstance(handler, _SizedTimedRotatingFileHandler)
        ]
        assert len(file_handlers) == 1
    finally:
        for handler in root.handlers:
            handler.close()
        root.handlers = original
