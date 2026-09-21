from collections import Counter
from typing import Dict
from .ai_threat_analyzer import AIThreatAnalyzer


class RiskEngine:
    """
    Calculates a risk score based on
    deception-environment events.
    """
    def __init__(self):
        self.ai_analyzer = AIThreatAnalyzer()

    EVENT_SCORES: Dict[str, int] = {
        "SESSION_STARTED": 0,

        # Discovery
        "IDENTITY_DISCOVERY": 8,
        "DIRECTORY_DISCOVERY": 10,
        "PROJECT_DIRECTORY_ACCESS": 10,
        "REPOSITORY_DISCOVERY": 15,

        # Access
        "DIRECTORY_ACCESS": 8,
        "REPOSITORY_ACCESS": 15,
        "FILE_ACCESS": 12,

        # High-value activity
        "COMMIT_HISTORY_ACCESS": 20,
        "SENSITIVE_FILE_ACCESS": 25,

        # File activity
        "DECOY_FILE_CREATED": 8,
        "DECOY_FILE_MODIFIED": 15,
        "DECOY_FILE_DELETED": 18,
    }

    SEVERITY_MULTIPLIER = {
        "LOW": 1.0,
        "MEDIUM": 1.15,
        "HIGH": 1.30,
        "CRITICAL": 1.50,
    }

    def calculate_event_score(self, event_type: str) -> int:
        return self.EVENT_SCORES.get(event_type, 5)

    def calculate_session_score(self, events: list):

        score = 0
        breakdown = []
        event_counter = Counter()

        for event in events:

            event_type = event.get(
                "event_type",
                ""
            )

            severity = event.get(
                "severity",
                "LOW"
            ).upper()

            base_score = self.calculate_event_score(
                event_type
            )

            multiplier = self.SEVERITY_MULTIPLIER.get(
                severity,
                1.0
            )

            event_score = round(
                base_score * multiplier
            )

            score += event_score

            event_counter[event_type] += 1

            breakdown.append({
                "event_type": event_type,
                "base_score": base_score,
                "severity": severity,
                "multiplier": multiplier,
                "score": event_score,
            })

        # --------------------------------
        # DISCOVERY + ACCESS BONUS
        # --------------------------------

        discovery_events = {
            "IDENTITY_DISCOVERY",
            "DIRECTORY_DISCOVERY",
            "PROJECT_DIRECTORY_ACCESS",
            "REPOSITORY_DISCOVERY",
        }

        access_events = {
            "FILE_ACCESS",
            "DIRECTORY_ACCESS",
            "REPOSITORY_ACCESS",
            "SENSITIVE_FILE_ACCESS",
            "COMMIT_HISTORY_ACCESS",
        }

        has_discovery = any(
            event_counter[event_type] > 0
            for event_type in discovery_events
        )

        has_access = any(
            event_counter[event_type] > 0
            for event_type in access_events
        )

        if has_discovery and has_access:

            score += 10

            breakdown.append({
                "event_type": "DISCOVERY_TO_ACCESS_BONUS",
                "base_score": 10,
                "severity": "BONUS",
                "multiplier": 1.0,
                "score": 10,
            })

        # --------------------------------
        # REPOSITORY ACTIVITY BONUS
        # --------------------------------

        repository_events = (
            event_counter["REPOSITORY_DISCOVERY"]
            + event_counter["REPOSITORY_ACCESS"]
            + event_counter["COMMIT_HISTORY_ACCESS"]
        )

        if repository_events >= 2:

            score += 10

            breakdown.append({
                "event_type": "REPOSITORY_ACTIVITY_BONUS",
                "base_score": 10,
                "severity": "BONUS",
                "multiplier": 1.0,
                "score": 10,
            })

        # --------------------------------
        # MULTIPLE EVENT BONUS
        # --------------------------------

        if len(events) >= 5:

            score += 5

            breakdown.append({
                "event_type": "MULTIPLE_EVENT_BONUS",
                "base_score": 5,
                "severity": "BONUS",
                "multiplier": 1.0,
                "score": 5,
            })

        return min(score, 100), breakdown

    def get_risk_level(self, score: int) -> str:

        if score <= 20:
            return "LOW"

        if score <= 50:
            return "MEDIUM"

        if score <= 80:
            return "HIGH"

        return "CRITICAL"

    def analyze(self, events: list):

        score, breakdown = self.calculate_session_score(
            events
        )

        ai_analysis = self.ai_analyzer.analyze(
            events,
            risk_score=score,
        )

        level = self.get_risk_level(
            score
        )

        behavior_indicators = []
        detections = []

        event_types = {
            event.get("event_type", "")
            for event in events
        }

        # --------------------------------
        # BEHAVIOR DETECTION
        # --------------------------------

        discovery_count = sum(
            1
            for event in events
            if event.get("event_type") in {
                "IDENTITY_DISCOVERY",
                "DIRECTORY_DISCOVERY",
                "PROJECT_DIRECTORY_ACCESS",
                "REPOSITORY_DISCOVERY",
            }
        )

        if discovery_count >= 2:

            description = (
                "Multiple internal resources discovered."
            )

            behavior_indicators.append(
                description
            )

            detections.append({
                "detected": True,
                "severity": "MEDIUM",
                "description": description,
            })

        if "REPOSITORY_DISCOVERY" in event_types:

            description = (
                "Internal repository enumeration detected."
            )

            behavior_indicators.append(
                description
            )

            detections.append({
                "detected": True,
                "severity": "HIGH",
                "description": description,
            })

        if "COMMIT_HISTORY_ACCESS" in event_types:

            description = (
                "Repository commit history accessed."
            )

            behavior_indicators.append(
                description
            )

            detections.append({
                "detected": True,
                "severity": "HIGH",
                "description": description,
            })

        high_value_events = {
            "REPOSITORY_ACCESS",
            "COMMIT_HISTORY_ACCESS",
            "SENSITIVE_FILE_ACCESS",
        }

        accessed_high_value = [
            event.get("event_type")
            for event in events
            if event.get("event_type")
            in high_value_events
        ]

        if accessed_high_value:

            description = (
                "High-value internal resources accessed."
            )

            behavior_indicators.append(
                description
            )

            detections.append({
                "detected": True,
                "severity": "HIGH",
                "description": description,
                "events": accessed_high_value,
            })

        if discovery_count >= 2 and accessed_high_value:

            description = (
                "Possible systematic reconnaissance "
                "pattern detected."
            )

            behavior_indicators.append(
                description
            )

            detections.append({
                "detected": True,
                "severity": "CRITICAL",
                "description": description,
            })

        # --------------------------------
        # MITRE ATT&CK MAPPING
        # --------------------------------

        mitre_techniques = []

        if any(
            event.get("event_type") in {
                "DIRECTORY_DISCOVERY",
                "PROJECT_DIRECTORY_ACCESS",
                "REPOSITORY_DISCOVERY",
            }
            for event in events
        ):

            mitre_techniques.append({
                "technique": "T1083",
                "name": "File and Directory Discovery",
                "tactic": "Discovery",
            })

        if any(
            event.get("event_type") in {
                "FILE_ACCESS",
                "REPOSITORY_ACCESS",
                "COMMIT_HISTORY_ACCESS",
                "SENSITIVE_FILE_ACCESS",
            }
            for event in events
        ):

            mitre_techniques.append({
                "technique": "T1005",
                "name": "Data from Local System",
                "tactic": "Collection",
            })

        behavior = {
            "event_count": len(events),
            "detections": detections,
            "suspicious": len(detections) > 0,
        }

        return {
            "score": score,
            "level": level,
            "event_count": len(events),
            "behavior": behavior,
            "behavior_indicators": behavior_indicators,
            "mitre_techniques": mitre_techniques,
            "risk_breakdown": breakdown,
            "ai_analysis": ai_analysis,
        }