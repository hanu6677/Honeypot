import json
from datetime import datetime, timezone

from .config import LOG_DIR


EVENT_LOG = LOG_DIR / "events.json"


def record_event(
    event_type: str,
    description: str,
    severity: str = "LOW",
    session_id: str = "LOCAL-TEST",
):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "event_type": event_type,
        "severity": severity,
        "description": description,
    }

    events = []

    if EVENT_LOG.exists():
        try:
            events = json.loads(
                EVENT_LOG.read_text(encoding="utf-8")
            )
        except json.JSONDecodeError:
            events = []

    events.append(event)

    EVENT_LOG.write_text(
        json.dumps(events, indent=4),
        encoding="utf-8",
    )

    print(
        f"[EVENT] {event_type} | "
        f"{severity} | {description}"
    )

    return event