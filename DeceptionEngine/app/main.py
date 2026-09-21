from .session import Session
from .events import record_event
from .risk_engine import RiskEngine
from .report_generator import SecurityReportGenerator


def main():

    print("=" * 60)
    print("      DECEPTION-AS-A-SERVICE")
    print("      Autonomous Honeypot Generator")
    print("=" * 60)

    # -----------------------------
    # START SESSION
    # -----------------------------

    session = Session(
        source="LOCAL-WINDOWS-TEST"
    )

    print(
        f"\n[+] Session started: "
        f"{session.session_id}"
    )

    # -----------------------------
    # TEST EVENTS
    # -----------------------------

    events = []

    events.append(
        record_event(
            event_type="PROJECT_DIRECTORY_ACCESS",
            description="Decoy project directory accessed.",
            severity="MEDIUM",
            session_id=session.session_id,
        )
    )

    events.append(
        record_event(
            event_type="REPOSITORY_DISCOVERY",
            description="Internal decoy repository discovered.",
            severity="HIGH",
            session_id=session.session_id,
        )
    )

    events.append(
        record_event(
            event_type="REPOSITORY_ACCESS",
            description="Decoy repository accessed.",
            severity="HIGH",
            session_id=session.session_id,
        )
    )

    events.append(
        record_event(
            event_type="COMMIT_HISTORY_ACCESS",
            description="Repository commit history accessed.",
            severity="HIGH",
            session_id=session.session_id,
        )
    )

    # -----------------------------
    # END SESSION
    # -----------------------------

    session.end()

    print(
        f"\n[+] Session ended: "
        f"{session.session_id}"
    )

    # -----------------------------
    # RISK ANALYSIS
    # -----------------------------

    risk_engine = RiskEngine()

    analysis = risk_engine.analyze(
        events
    )

    # -----------------------------
    # GENERATE REPORT
    # -----------------------------

    generator = SecurityReportGenerator()

    report_text, report_path = generator.generate(
        session,
        events,
        analysis,
    )

    print("\n" + report_text)

    print(
        f"\n[+] Security report saved to:"
        f"\n    {report_path}"
    )


if __name__ == "__main__":
    main()