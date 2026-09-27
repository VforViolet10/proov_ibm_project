# config_loader.py
# Reads settings.cfg. Hand-rolled parser kept for backward compatibility.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict:
    """Load key=value pairs from *path* (defaults to settings.cfg).

    Only keys listed in KNOWN_KEYS are retained; unknown keys are silently
    dropped (a legacy behaviour preserved for compatibility).
    """
    if path is None:
        path = SETTINGS_FILE
    settings: dict = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            parts = line.split("=")
            key = parts[0].strip()
            value = parts[1].strip()
            if key in KNOWN_KEYS:
                settings[key] = value   # all values stay strings; callers convert
    return settings


def get_int(settings: dict, key: str, fallback: int) -> int:
    """Return settings[key] as int, or fallback if missing or non-numeric."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict, key: str, fallback: str = "") -> str:
    """Return settings[key], or fallback when the key is absent."""
    return settings.get(key, fallback)
