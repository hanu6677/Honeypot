from datetime import datetime, timezone
from pathlib import Path


REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"


class SecurityReportGenerator:

    def __init__(self, report_dir=REPORT_DIR):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def generate(self, session, events, analysis):

        session_info = session.info()

        report = []

        report.append("=" * 60)
        report.append("             DECEPTION SECURITY REPORT")
        report.append("=" * 60)

        report.append("")
        report.append("SESSION INFORMATION")
        report.append("-" * 60)

        report.append(
            f"Session ID : {session_info['session_id']}"
        )

        report.append(
            f"Source     : {session_info['source']}"
        )

        report.append(
            f"Start Time : {session_info['start_time']}"
        )

        report.append(
            f"End Time   : {session_info['end_time']}"
        )

        report.append("")

        report.append("RISK ASSESSMENT")
        report.append("-" * 60)

        report.append(
            f"Risk Score : {analysis['score']}/100"
        )

        report.append(
            f"Risk Level : {analysis['level']}"
        )

        report.append(
            f"Events     : {analysis['event_count']}"
        )

        report.append("")

        report.append("BEHAVIOR ANALYSIS")
        report.append("-" * 60)

        behavior = analysis.get("behavior", {})

        if behavior.get("suspicious"):
            report.append("Status     : SUSPICIOUS")
        else:
            report.append("Status     : NORMAL")

        detections = behavior.get(
            "detections",
            []
        )

        if detections:

            for detection in detections:

                severity = detection.get(
                    "severity",
                    "UNKNOWN"
                )

                description = detection.get(
                    "description",
                    "No description"
                )

                report.append(
                    f"[{severity}] {description}"
                )

        else:

            report.append(
                "No suspicious behavior detected."
            )

        report.append("")

        report.append("BEHAVIOR INDICATORS")
        report.append("-" * 60)

        indicators = analysis.get(
            "behavior_indicators",
            []
        )

        if indicators:

            for indicator in indicators:
                report.append(
                    f"• {indicator}"
                )

        else:

            report.append(
                "No behavior indicators."
            )

        report.append("")

        report.append("MITRE ATT&CK MAPPING")
        report.append("-" * 60)

        techniques = analysis.get(
            "mitre_techniques",
            []
        )

        if techniques:

            for technique in techniques:

                report.append(
                    f"{technique.get('technique')} | "
                    f"{technique.get('name')} | "
                    f"{technique.get('tactic')}"
                )

        else:

            report.append(
                "No MITRE ATT&CK techniques mapped."
            )

        report.append("")

        report.append("EVENT SUMMARY")
        report.append("-" * 60)

        for index, event in enumerate(events, 1):

            report.append(
                f"{index}. "
                f"{event.get('event_type')} | "
                f"{event.get('severity')} | "
                f"{event.get('description')}"
            )

        report.append("")

        report.append("RECOMMENDATIONS")
        report.append("-" * 60)

        recommendations = self.generate_recommendations(
            analysis
        )

        for recommendation in recommendations:

            report.append(
                f"• {recommendation}"
            )

        report.append("")
        report.append("=" * 60)
        report.append(
            "Report generated at: "
            f"{datetime.now(timezone.utc).isoformat()}"
        )
        report.append("=" * 60)

        report_text = "\n".join(report)

        filename = (
            f"{session_info['session_id']}_report.txt"
        )

        report_path = self.report_dir / filename

        report_path.write_text(
            report_text,
            encoding="utf-8"
        )

        return report_text, report_path

    def generate_recommendations(self, analysis):

        score = analysis.get("score", 0)
        level = analysis.get("level", "LOW")

        recommendations = []

        if score >= 80:

            recommendations.append(
                "Investigate the session as a high-priority security event."
            )

            recommendations.append(
                "Review all decoy resources accessed during the session."
            )

        elif score >= 50:

            recommendations.append(
                "Review the observed activity and session timeline."
            )

            recommendations.append(
                "Monitor for repeated access attempts."
            )

        elif score >= 20:

            recommendations.append(
                "Continue monitoring the session for additional activity."
            )

        else:

            recommendations.append(
                "No immediate action required; continue monitoring."
            )
        if level == "CRITICAL":

            recommendations.append(
                "Escalate the event for security investigation."
            )

        return recommendations