import time
import hashlib
from pathlib import Path

from .events import record_event
from .security_pipeline import SecurityPipeline


class DecoyFileMonitor:

    def __init__(self, watch_directory, session_id, pipeline=None):
        self.watch_directory = Path(watch_directory)
        self.session_id = session_id
        self.pipeline = pipeline or SecurityPipeline()
        self.known_files = self.get_files()

    def get_file_state(self, file_path):
        try:
            stat = file_path.stat()

            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            return {
                "mtime": stat.st_mtime_ns,
                "hash": file_hash
            }

        except (OSError, PermissionError):
            return None

    def get_files(self):
        files = {}

        for file_path in self.watch_directory.rglob("*"):
            if file_path.is_file():
                state = self.get_file_state(file_path)

                if state:
                    files[file_path] = state

        return files

    def record_activity(self, event_type, description, severity):

        event = record_event(
            event_type=event_type,
            description=description,
            severity=severity,
            session_id=self.session_id
        )

        self.pipeline.add_event(event)

    def check_changes(self):

        current_files = self.get_files()

        # CREATED
        for file_path in current_files:

            if file_path not in self.known_files:

                self.record_activity(
                    "DECOY_FILE_CREATED",
                    f"New decoy file created: {file_path}",
                    "MEDIUM"
                )

        # DELETED
        for file_path in self.known_files:

            if file_path not in current_files:

                self.record_activity(
                    "DECOY_FILE_DELETED",
                    f"Decoy file deleted: {file_path}",
                    "HIGH"
                )

        # MODIFIED
        for file_path in current_files:

            if file_path in self.known_files:

                old_state = self.known_files[file_path]
                new_state = current_files[file_path]

                if (
                    old_state["mtime"] != new_state["mtime"]
                    or old_state["hash"] != new_state["hash"]
                ):

                    self.record_activity(
                        "DECOY_FILE_MODIFIED",
                        f"Decoy file modified: {file_path}",
                        "HIGH"
                    )

        self.known_files = current_files

    def start(self, interval=2):

        print(f"[+] Monitoring decoy environment:")
        print(f"    {self.watch_directory}")

        try:

            while True:
                self.check_changes()
                time.sleep(interval)

        except KeyboardInterrupt:

            print("\n[+] File monitor stopped.")