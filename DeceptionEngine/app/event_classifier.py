EVENT_CLASSIFICATION = {

    "DECOY_FILE_CREATED": {
        "category": "FILE_ACTIVITY",
        "severity": "MEDIUM",
        "description": "A new file was created inside the decoy environment.",
    },

    "DECOY_FILE_MODIFIED": {
        "category": "FILE_ACTIVITY",
        "severity": "HIGH",
        "description": "A decoy file was modified.",
    },

    "DECOY_FILE_DELETED": {
        "category": "FILE_ACTIVITY",
        "severity": "HIGH",
        "description": "A decoy file was deleted.",
    },

    "PROJECT_DIRECTORY_ACCESS": {
        "category": "DISCOVERY",
        "severity": "MEDIUM",
        "description": "A decoy project directory was accessed.",
    },

    "REPOSITORY_DISCOVERY": {
        "category": "DISCOVERY",
        "severity": "HIGH",
        "description": "A decoy repository was discovered.",
    },

    "REPOSITORY_ACCESS": {
        "category": "RESOURCE_ACCESS",
        "severity": "HIGH",
        "description": "A decoy repository was accessed.",
    },

    "COMMIT_HISTORY_ACCESS": {
        "category": "RESOURCE_ACCESS",
        "severity": "HIGH",
        "description": "Repository commit history was accessed.",
    },
}


def classify_event(event_type: str):
    normalized_event_type = (event_type or "").upper()

    return EVENT_CLASSIFICATION.get(
        normalized_event_type,
        {
            "category": "UNKNOWN",
            "severity": "LOW",
            "description": "Unknown event detected.",
        },
    )


def enrich_event(event: dict):
    if not isinstance(event, dict):
        return event

    normalized_event = dict(event)
    normalized_event_type = str(normalized_event.get("event_type", "")).upper()
    normalized_event["event_type"] = normalized_event_type

    classification = classify_event(normalized_event_type)
    normalized_event.setdefault("category", classification["category"])
    normalized_event.setdefault("severity", classification["severity"])
    normalized_event.setdefault("description", classification["description"])

    return normalized_event