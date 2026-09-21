import unittest

from app.event_classifier import classify_event, enrich_event
from app.risk_engine import RiskEngine


class EventClassifierTests(unittest.TestCase):
    def test_classify_known_event(self):
        classification = classify_event("DECOY_FILE_MODIFIED")

        self.assertEqual(classification["category"], "FILE_ACTIVITY")
        self.assertEqual(classification["severity"], "HIGH")
        self.assertIn("modified", classification["description"].lower())

    def test_enrich_event_uses_default_classification(self):
        event = enrich_event({"event_type": "DECOY_FILE_CREATED"})

        self.assertEqual(event["category"], "FILE_ACTIVITY")
        self.assertEqual(event["severity"], "MEDIUM")
        self.assertIn("created", event["description"].lower())

    def test_risk_engine_integrates_ai_analysis(self):
        analysis = RiskEngine().analyze([
            {"event_type": "PROJECT_DIRECTORY_ACCESS", "severity": "MEDIUM"},
            {"event_type": "REPOSITORY_DISCOVERY", "severity": "HIGH"},
            {"event_type": "REPOSITORY_ACCESS", "severity": "HIGH"},
            {"event_type": "COMMIT_HISTORY_ACCESS", "severity": "HIGH"},
        ])

        self.assertIn("ai_analysis", analysis)
        self.assertIn("threat", analysis["ai_analysis"])
        self.assertIn("confidence", analysis["ai_analysis"])
        self.assertGreaterEqual(analysis["ai_analysis"]["confidence"], 0.0)


if __name__ == "__main__":
    unittest.main()
