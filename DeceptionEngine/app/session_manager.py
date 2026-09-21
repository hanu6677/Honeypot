from .session import Session
class SessionManager:
    def __init__(self):
        self.current_session = None
    def start_session(self, source="LOCAL-WINDOWS-TEST"):
        if self.current_session is not None:
            return self.current_session
        self.current_session = Session(
            source=source
        )
        print(
            f"[+] Session started: "
            f"{self.current_session.session_id}"
        )
        return self.current_session
    def end_session(self):
        if self.current_session is None:
            return None
        self.current_session.end()
        print(
            f"[+] Session ended: "
            f"{self.current_session.session_id}"
        )
        session = self.current_session
        self.current_session = None
        return session
    def get_current_session(self):
        return self.current_session
    def is_active(self):
        return self.current_session is not None