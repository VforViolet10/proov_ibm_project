# fleet_utils.py
# Catch-all helpers since 2013.

# BUG FIXED: was 1.609 (km-per-mile, inverted). Correct value is 0.621371 miles-per-km.
MILES_PER_KM = 0.621371


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles. Used by the nightly UK partner report."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a number to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a number as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list) -> float:
    """Return the arithmetic mean of a list of numbers, or 0 for an empty list."""
    total = 0.0
    count = 0
    for v in values:
        total += v
        count += 1
    if count == 0:
        return 0.0
    return total / count


def is_due(pct: float, threshold: float) -> bool:
    """Return True when pct >= threshold."""
    return pct >= threshold


def parse_service_date(text: str):
    """Parse a DD.MM.YYYY date string and return (year, month, day), or None."""
    parts = text.split(".")
    if len(parts) != 3:
        return None
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    return (year, month, day)


def chunk_list(items: list, size: int) -> list:
    """Split a list into chunks of at most *size* items each."""
    chunks = []
    current = []
    for item in items:
        current.append(item)
        if len(current) == size:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks
