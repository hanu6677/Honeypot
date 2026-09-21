from .session_manager import SessionManager
from .security_pipeline import SecurityPipeline
from .events import record_event


manager = SessionManager()
pipeline = SecurityPipeline()

# Start session
session = manager.start_session(
    source="LOCAL-WINDOWS-TEST"
)

# Event 1
event = record_event(
    event_type="PROJECT_DIRECTORY_ACCESS",
    description="Decoy project directory accessed.",
    severity="MEDIUM",
    session_id=session.session_id,
)

pipeline.add_event(event)

# Event 2
event = record_event(
    event_type="REPOSITORY_DISCOVERY",
    description="Internal decoy repository discovered.",
    severity="HIGH",
    session_id=session.session_id,
)

pipeline.add_event(event)

# Event 3
event = record_event(
    event_type="REPOSITORY_ACCESS",
    description="Decoy repository accessed.",
    severity="HIGH",
    session_id=session.session_id,
)

pipeline.add_event(event)

# Event 4
event = record_event(
    event_type="COMMIT_HISTORY_ACCESS",
    description="Repository commit history accessed.",
    severity="HIGH",
    session_id=session.session_id,
)

pipeline.add_event(event)

# End session
manager.end_session()

# Analyze + Generate Report
result = pipeline.finish_session(session)

print()
print("=" * 60)
print("PIPELINE RESULT")
print("=" * 60)

print(
    f"Risk Score : "
    f"{result['analysis']['score']}/100"
)

print(
    f"Risk Level : "
    f"{result['analysis']['level']}"
)

print(
    f"Report     : "
    f"{result['report_path']}"
)
