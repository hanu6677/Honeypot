import uuid
from datetime import datetime, timezone


class Session:
    def __init__(self, source="LOCAL-TEST"):
        self.session_id = f"SES-{uuid.uuid4().hex[:8].upper()}"
        self.source = source
        self.start_time = datetime.now(timezone.utc)
        self.end_time = None
        self.active = True

    def end(self):
        self.end_time = datetime.now(timezone.utc)
        self.active = False

    def info(self):
        return {
            "session_id": self.session_id,
            "source": self.source,
            "start_time": self.start_time.isoformat(),
            "end_time": (
                self.end_time.isoformat()
                if self.end_time
                else None
            ),
            "active": self.active,
        }