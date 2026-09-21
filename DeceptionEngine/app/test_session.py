from app.session_manager import SessionManager
from app.events import record_event
manager = SessionManager()
# Start session
session = manager.start_session(
    source="LOCAL-WINDOWS-TEST"
)


# Generate events using the session ID


record_event(
    event_type="PROJECT_DIRECTORY_ACCESS",
    description="Decoy project directory accessed.",
    severity="MEDIUM",
    session_id=session.session_id,
)
record_event(
    event_type="REPOSITORY_DISCOVERY",
    description="Internal decoy repository discovered.",
    severity="HIGH",
    session_id=session.session_id,
)
record_event(
    event_type="REPOSITORY_ACCESS",
    description="Decoy repository accessed.",
    severity="HIGH",
    session_id=session.session_id,
)
# End session
manager.end_session()