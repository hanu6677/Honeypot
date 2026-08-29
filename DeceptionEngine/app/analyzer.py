import json

from .config import LOG_DIR
from .risk_engine import RiskEngine
from .mitre import map_events

EVENT_LOG = LOG_DIR / "events.json"


def load_events():
    if not EVENT_LOG.exists():
        return []

    try:
        return json.loads(
            EVENT_LOG.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError:
        return []


def analyze_session(session_id: str):
    events = load_events()

    session_events = [
        event
        for event in events
        if event.get("session_id") == session_id
    ]

    engine = RiskEngine()

    analysis = engine.analyze(session_events)

    analysis["mitre_techniques"] = map_events(session_events)

    return analysis

    engine = RiskEngine()

    return engine.analyze(session_events)