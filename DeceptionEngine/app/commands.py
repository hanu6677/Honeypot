from .config import DECOY_ROOT
from .events import record_event
class CommandEngine:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.current_dir = DECOY_ROOT
    def prompt_path(self):
        try:
            relative = self.current_dir.relative_to(DECOY_ROOT)
            if str(relative) == ".":
                return "C:\\"
            return "C:\\" + str(relative).replace("/", "\\")
        except ValueError:
            return "C:\\"
    def execute(self, command: str):
        command = command.strip()
        if not command:
            return ""
        parts = command.split(maxsplit=1)
        action = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""
        if action in ("dir", "ls"):
            return self.list_directory()
        if action == "cd":
            return self.change_directory(argument)
        if action in ("type", "cat"):
            return self.read_file(argument)
        if action == "whoami":
            return self.whoami()
        if action == "pwd":
            return self.prompt_path()
        return f"'{action}' is not available in the deception environment."
    def list_directory(self):
        items = sorted(self.current_dir.iterdir())
        record_event(
            event_type="DIRECTORY_DISCOVERY",
            description=f"Listed directory: {self.prompt_path()}",
            severity="MEDIUM",
            session_id=self.session_id,
        )
        output = []
        for item in items:
            if item.is_dir():
                output.append(f"<DIR>  {item.name}")
            else:
                output.append(f"        {item.name}")
        return "\n".join(output)
    def change_directory(self, argument):
        if not argument:
            return self.prompt_path() 
        if argument == "..":
            if self.current_dir != DECOY_ROOT:
                self.current_dir = self.current_dir.parent
            return self.prompt_path()
        target = self.current_dir / argument
        if not target.exists():
            return f"The system cannot find the path specified: {argument}"
        if not target.is_dir():
            return f"Not a directory: {argument}"
        self.current_dir = target
        record_event(
            event_type="DIRECTORY_ACCESS",
            description=f"Changed directory to: {self.prompt_path()}",
            severity="MEDIUM",
            session_id=self.session_id,
        )
        return self.prompt_path()
    def read_file(self, argument):
        if not argument:
            return "The syntax of the command is incorrect."
        target = self.current_dir / argument
        if not target.exists():
            return f"The system cannot find the file specified: {argument}"
        if not target.is_file():
            return f"Not a file: {argument}"
        content = target.read_text(encoding="utf-8")
        record_event(
            event_type="FILE_ACCESS",
            description=f"Read file: {self.prompt_path()}\\{argument}",
            severity="HIGH",
            session_id=self.session_id,
        )
        return content
    def whoami(self):
        record_event(
            event_type="IDENTITY_DISCOVERY",
            description="User identity queried",
            severity="MEDIUM",
            session_id=self.session_id,
        )
        return "company\\developer"