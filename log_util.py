# log_util.py
# A homemade logger (the logging module felt like "too much magic" in 2013).

import time

LOG_LINES: list[str] = []   # global buffer, shared by every importer
DEBUG = False


def log(message: str) -> None:
    """Append a timestamped line to the in-memory buffer and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a DEBUG-level message (only when DEBUG is True)."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Write buffered log lines to *path* (append mode) and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    del LOG_LINES[:]
