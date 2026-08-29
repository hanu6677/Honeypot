from datetime import datetime, timezone
def build_request_event(
    session_id: str,
    client_ip: str,
    method: str,
    path: str,
    user_agent: str,
    status_code: int,
):
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": "HTTP_REQUEST",
        "session_id": session_id,
        "source_ip": client_ip,
        "method": method,
        "path": path,
        "user_agent": user_agent,
        "status_code": status_code,
    }