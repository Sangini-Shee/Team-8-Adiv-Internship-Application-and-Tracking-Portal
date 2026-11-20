
import json
from datetime import datetime, timezone
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"
AUDIT_FILE = OUTPUT_DIR / "audit_log.jsonl"


def record_audit_event(event, details):
    """Store a governance event in a JSON Lines audit file."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "details": details
    }

    with open(AUDIT_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(record, default=str) + "\n")

    return record


def read_audit_logs():
    """Read all recorded audit events."""

    if not AUDIT_FILE.exists():
        return []

    records = []

    with open(AUDIT_FILE, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records
