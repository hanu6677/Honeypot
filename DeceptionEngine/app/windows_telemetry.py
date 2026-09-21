import subprocess
from datetime import datetime, timezone

from .events import record_event


def get_recent_security_events(max_events=20):

    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        f"Get-WinEvent -LogName Security -MaxEvents {max_events} "
        "| Select-Object TimeCreated, Id, ProviderName, Message "
        "| ConvertTo-Json -Depth 3"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
            or "Unable to read Windows Security log."
        )

    if not result.stdout.strip():
        return []

    return result.stdout


def test_security_log():

    try:

        events = get_recent_security_events()

        record_event(
            event_type="WINDOWS_TELEMETRY_TEST",
            description="Windows Security Event Log successfully queried.",
            severity="LOW",
            session_id="WINDOWS-TEST",
        )

        print("[+] Windows Security telemetry is accessible.")
        print(events)

        return True

    except Exception as error:

        print(
            f"[-] Windows telemetry error: {error}"
        )

        return False


if __name__ == "__main__":
    test_security_log()