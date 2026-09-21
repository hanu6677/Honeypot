"""
AI Threat Analyzer
Provides AI-ready threat analysis for the deception/honeypot system.
The analyzer:
1. Extracts behavioral indicators from security events.
2. Generates a threat hypothesis.
3. Calculates confidence.
4. Provides an explanation and recommended action.
5. Works without an external AI API as a safe fallback.
Later, an LLM provider can be connected without changing the rest
of the security pipeline.
"""
from collections import Counter
class AIThreatAnalyzer:
    def __init__(self):
        self.high_risk_events = {
            "DECOY_FILE_DELETED",
            "DECOY_FILE_MODIFIED",
            "REPOSITORY_ACCESS",
            "COMMIT_HISTORY_ACCESS",
            "HIGH_VALUE_ACCESS",
        }
        self.discovery_events = {
            "DIRECTORY_DISCOVERY",
            "REPOSITORY_DISCOVERY",
            "FILE_DISCOVERY",
            "PROJECT_DIRECTORY_ACCESS",
        }
        self.credential_events = {
            "CREDENTIAL_ACCESS",
            "SECRET_ACCESS",
            "CONFIG_ACCESS",
        }
    def analyze(self, events, risk_score=0):
        """
        Analyze a list of security events.
        Args:
            events: List of event dictionaries.
            risk_score: Existing score from RiskEngine.
        Returns:
            Dictionary containing AI-ready threat analysis.
        """
        if not events:
            return self._no_activity_result()
        event_types = [
            event.get("event_type", "").upper()
            for event in events
        ]
        counts = Counter(event_types)
        discovery_count = sum(
            counts[event]
            for event in self.discovery_events
        )
        high_risk_count = sum(
            counts[event]
            for event in self.high_risk_events
        )
        credential_count = sum(
            counts[event]
            for event in self.credential_events
        )
        behavioral_indicators = {
            "discovery_activity": discovery_count > 0,
            "repository_activity": any(
                "REPOSITORY" in event
                for event in event_types
            ),
            "high_value_activity": high_risk_count > 0,
            "credential_activity": credential_count > 0,
            "file_tampering": any(
                event in {
                    "DECOY_FILE_MODIFIED",
                    "DECOY_FILE_DELETED",
                }
                for event in event_types
            ),
        }
        threat, severity = self._classify_threat(
            behavioral_indicators,
            risk_score,
        )
        confidence = self._calculate_confidence(
            behavioral_indicators,
            len(events),
            risk_score,
        )
        explanation = self._generate_explanation(
            behavioral_indicators,
            counts,
            risk_score,
        )
        recommendation = self._recommend_action(
            severity,
            behavioral_indicators,
        )
        return {
            "threat": threat,
            "severity": severity,
            "confidence": round(confidence, 2),
            "risk_score": risk_score,
            "behavioral_indicators": behavioral_indicators,
            "event_summary": dict(counts),
            "explanation": explanation,
            "recommended_action": recommendation,
        }
    def _classify_threat(self, indicators, risk_score):
        if indicators["credential_activity"]:
            return (
                "Possible Credential/Secret Access",
                "CRITICAL",
            )
        if (
            indicators["file_tampering"]
            and indicators["high_value_activity"]
        ):
            return (
                "Possible Malicious Data Manipulation",
                "CRITICAL",
            )
        if (
            indicators["discovery_activity"]
            and indicators["repository_activity"]
        ):
            return (
                "Possible Internal Reconnaissance",
                "HIGH",
            )
        if indicators["high_value_activity"]:
            return (
                "Suspicious High-Value Resource Access",
                "HIGH",
            )
        if indicators["discovery_activity"]:
            return (
                "Possible Reconnaissance Activity",
                "MEDIUM",
            )
        if risk_score >= 70:
            return (
                "Potential Security Threat",
                "HIGH",
            )
        if risk_score >= 40:
            return (
                "Suspicious Activity",
                "MEDIUM",
            )
        return (
            "Low-Risk Activity",
            "LOW",
        )
    def _calculate_confidence(
        self,
        indicators,
        event_count,
        risk_score,
    ):
        confidence = 0.25
        active_indicators = sum(
            1
            for value in indicators.values()
            if value
        )
        confidence += active_indicators * 0.12
        if event_count >= 3:
            confidence += 0.10
        if event_count >= 5:
            confidence += 0.08
        if risk_score >= 70:
            confidence += 0.10
        elif risk_score >= 40:
            confidence += 0.05
        return min(confidence, 0.99)
    def _generate_explanation(
        self,
        indicators,
        event_counts,
        risk_score,
    ):
        reasons = []
        if indicators["discovery_activity"]:
            reasons.append(
                "discovery activity was observed"
            )
        if indicators["repository_activity"]:
            reasons.append(
                "repository-related resources were accessed"
            )
        if indicators["high_value_activity"]:
            reasons.append(
                "high-value decoy resources were accessed"
            )
        if indicators["credential_activity"]:
            reasons.append(
                "credential or secret-related resources were accessed"
            )
        if indicators["file_tampering"]:
            reasons.append(
                "decoy files were modified or deleted"
            )
        if not reasons:
            return (
                "No strong malicious behavioral pattern was "
                "identified from the observed events."
            )
        explanation = (
            "The session is suspicious because "
            + ", ".join(reasons)
            + "."
        )
        if risk_score >= 70:
            explanation += (
                " The existing risk score is also high, "
                "which increases confidence in the assessment."
            )
        return explanation
    def _recommend_action(
        self,
        severity,
        indicators,
    ):
        if severity == "CRITICAL":
            return (
                "Immediately investigate the session, preserve "
                "telemetry, and consider isolating the affected "
                "decoy environment."
            )
        if severity == "HIGH":
            return (
                "Investigate the session and increase monitoring "
                "for additional suspicious activity."
            )
        if severity == "MEDIUM":
            return (
                "Continue monitoring the session and correlate "
                "future events for escalation."
            )
        return (
            "Continue normal monitoring. No immediate response "
            "is required."
        )
    def _no_activity_result(self):
        return {
            "threat": "No Suspicious Activity",
            "severity": "LOW",
            "confidence": 0.99,
            "risk_score": 0,
            "behavioral_indicators": {},
            "event_summary": {},
            "explanation": (
                "No security events were available for analysis."
            ),
            "recommended_action": (
                "Continue normal monitoring."
            ),
        }