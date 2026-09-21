from typing import List, Dict
class BehaviorAnalyzer:
    """
    Detects suspicious behavior patterns
    from honeypot session events.
    """
    DISCOVERY_EVENTS = {
        "IDENTITY_DISCOVERY",
        "DIRECTORY_DISCOVERY",
        "DIRECTORY_ACCESS",
        "EMPLOYEE_DIRECTORY_ACCESS",
        "PROJECT_DIRECTORY_ACCESS",
        "REPOSITORY_DISCOVERY",
    }
    HIGH_VALUE_EVENTS = {
        "SENSITIVE_FILE_ACCESS",
        "REPOSITORY_ACCESS",
        "COMMIT_HISTORY_ACCESS",
        "TICKET_DATABASE_ACCESS",
    }
    def __init__(self, events: List[Dict]):
        self.events = events
        self.event_types = [
            event.get("event_type", "")
            for event in events
        ]

    # ------------------------------------------------
    # Discovery analysis
    # ------------------------------------------------

    def detect_discovery(self):

        count = sum(
            1
            for event in self.event_types
            if event in self.DISCOVERY_EVENTS
        )

        if count >= 4:
            return {
                "detected": True,
                "severity": "HIGH",
                "description":
                    "Systematic internal resource discovery detected."
            }

        if count >= 2:
            return {
                "detected": True,
                "severity": "MEDIUM",
                "description":
                    "Multiple internal resources discovered."
            }

        return {
            "detected": False,
            "severity": "LOW",
            "description": None
        }

    # ------------------------------------------------
    # Repository enumeration
    # ------------------------------------------------

    def detect_repository_enumeration(self):

        if (
            "REPOSITORY_DISCOVERY" in self.event_types
            and "REPOSITORY_ACCESS" in self.event_types
        ):
            return {
                "detected": True,
                "severity": "HIGH",
                "description":
                    "Internal repository enumeration detected."
            }

        return {
            "detected": False,
            "severity": "LOW",
            "description": None
        }

    # ------------------------------------------------
    # Commit history access
    # ------------------------------------------------

    def detect_commit_access(self):

        if "COMMIT_HISTORY_ACCESS" in self.event_types:

            return {
                "detected": True,
                "severity": "HIGH",
                "description":
                    "Repository commit history accessed."
            }

        return {
            "detected": False,
            "severity": "LOW",
            "description": None
        }

    # ------------------------------------------------
    # High-value resource access
    # ------------------------------------------------

    def detect_high_value_access(self):

        found = [
            event
            for event in self.event_types
            if event in self.HIGH_VALUE_EVENTS
        ]

        if found:

            return {
                "detected": True,
                "severity": "HIGH",
                "description":
                    "High-value internal resources accessed.",
                "events": found
            }

        return {
            "detected": False,
            "severity": "LOW",
            "description": None,
            "events": []
        }

    # ------------------------------------------------
    # Reconnaissance pattern
    # ------------------------------------------------

    def detect_reconnaissance(self):

        required = {
            "PROJECT_DIRECTORY_ACCESS",
            "REPOSITORY_DISCOVERY",
            "COMMIT_HISTORY_ACCESS",
        }

        if required.issubset(
            set(self.event_types)
        ):

            return {
                "detected": True,
                "severity": "CRITICAL",
                "description":
                    "Possible systematic reconnaissance pattern detected."
            }

        return {
            "detected": False,
            "severity": "LOW",
            "description": None
        }

    # ------------------------------------------------
    # Run complete analysis
    # ------------------------------------------------

    def analyze(self):

        detections = []

        checks = [
            self.detect_discovery(),
            self.detect_repository_enumeration(),
            self.detect_commit_access(),
            self.detect_high_value_access(),
            self.detect_reconnaissance(),
        ]

        for result in checks:

            if result["detected"]:
                detections.append(result)

        return {
            "event_count": len(self.events),
            "detections": detections,
            "suspicious": len(detections) > 0,
        }


def analyze_behavior(events: List[Dict]) -> Dict:
    """
    Convenience function for the Risk Engine.
    """

    analyzer = BehaviorAnalyzer(events)

    return analyzer.analyze()