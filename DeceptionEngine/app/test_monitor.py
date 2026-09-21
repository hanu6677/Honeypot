from .decoy_filesystem import create_decoy_environment
from .file_monitor import DecoyFileMonitor
from .session import Session
from .security_pipeline import SecurityPipeline


def main():
    decoy_path = create_decoy_environment()

    session = Session(source="LOCAL-WINDOWS-TEST")
    pipeline = SecurityPipeline()

    monitor = DecoyFileMonitor(
        watch_directory=decoy_path,
        session_id=session.session_id,
        pipeline=pipeline
    )

    print("\n[+] Real-time honeypot monitoring started")
    print(f"[+] Session ID: {session.session_id}")
    print(f"[+] Watching: {decoy_path}")
    print("\n[+] Modify/create/delete files inside decoy_environment")
    print("[+] Press CTRL+C to stop monitoring.\n")

    try:
        monitor.start(interval=2)
    except KeyboardInterrupt:
        pass
    finally:
        session.end()

        result = pipeline.finish_session(session)

        print("\n" + "=" * 50)
        print("SECURITY RESULT")
        print("=" * 50)
        print("Risk Score :", result["analysis"]["score"])
        print("Risk Level :", result["analysis"]["level"])
        print("Events     :", result["analysis"]["event_count"])
        print("Report     :", result["report_path"])


if __name__ == "__main__":
    main()