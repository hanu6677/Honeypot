from .filesystem import build_environment
from .events import record_event
from .session import Session
from .commands import CommandEngine
from .analyzer import analyze_session
def main():
    print("=" * 55)
    print("       DECEPTION-AS-A-SERVICE")
    print("       Windows Deception Terminal")
    print("=" * 55)
    build_environment()
    session = Session(source="LOCAL-TEST")
    print(f"\n[+] Session started: {session.session_id}")
    record_event(
        event_type="SESSION_STARTED",
        description="New deception session started",
        severity="LOW",
        session_id=session.session_id,
    )
    terminal = CommandEngine(session.session_id)
    print("\nType 'exit' to close the session.\n")
    while True:
        try:
            command = input(
                f"{terminal.prompt_path()}> "
            )
            if command.lower() == "exit":
                break
            result = terminal.execute(command)
            if result:
                print(result)
        except KeyboardInterrupt:
            print("\n[!] Session interrupted.")
            break
    session.end()
    analysis = analyze_session(session.session_id)
    print("\n" + "=" * 55)
    print("             SESSION RISK REPORT")
    print("=" * 55)

    print(f"Session ID : {session.session_id}")
    print(f"Events     : {analysis['event_count']}")
    print(f"Risk Score : {analysis['score']}/100")
    print(f"Risk Level : {analysis['level']}")

    print("\nMITRE ATT&CK")
    print("-" * 55)

    for technique in analysis["mitre_techniques"]:
        print(
        f"{technique['technique']} | "
        f"{technique['name']} | "
        f"{technique['tactic']}"
    )

    print("=" * 55)
    print(f"Session ID : {session.session_id}")
    print(f"Events     : {analysis['event_count']}")    
    print(f"Risk Score : {analysis['score']}/100")
    print(f"Risk Level : {analysis['level']})")

    print("=" * 55)
    record_event(
        event_type="SESSION_ENDED",
        description="Deception session ended",
        severity="LOW",
        session_id=session.session_id,
    )
    print(f"\n[+] Session ended: {session.session_id}")
if __name__ == "__main__":
    main()