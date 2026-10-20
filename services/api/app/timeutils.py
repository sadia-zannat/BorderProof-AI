"""SQLite drops timezone metadata; API timestamps must still identify UTC."""
from datetime import timezone
def iso_utc(value):
    return (value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)).isoformat()
