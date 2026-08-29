from typing import Dict
class RiskEngine:
    """
    Calculates a risk score based on deception-environment events.
    """
    EVENT_SCORES: Dict[str, int] = {
        "SESSION_STARTED": 0,
        "IDENTITY_DISCOVERY": 10,
        "DIRECTORY_DISCOVERY": 10,
        "DIRECTORY_ACCESS": 10,
        "FILE_ACCESS": 15,
        "SENSITIVE_FILE_ACCESS": 30,
    }
    def calculate_event_score(self, event_type: str) -> int:
        return self.EVENT_SCORES.get(event_type, 5)
    def calculate_session_score(self, events: list) -> int:
        score = 0
        for event in events:
            event_type = event.get("event_type", "")
            score += self.calculate_event_score(event_type)
        return min(score, 100)
    def get_risk_level(self, score: int) -> str:
        if score <= 20:
            return "LOW"
        if score <= 50:
            return "MEDIUM"
        if score <= 80:
            return "HIGH"
        return "CRITICAL"
    def analyze(self, events: list) -> dict:
        score = self.calculate_session_score(events)
        level = self.get_risk_level(score)
        return {
            "score": score,
            "level": level,
            "event_count": len(events),
        }