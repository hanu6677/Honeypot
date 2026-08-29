MITRE_MAPPING = {
    "IDENTITY_DISCOVERY": {
        "technique": "T1033",
        "name": "System Owner/User Discovery",
        "tactic": "Discovery",
    },

    "DIRECTORY_DISCOVERY": {
        "technique": "T1083",
        "name": "File and Directory Discovery",
        "tactic": "Discovery",
    },

    "DIRECTORY_ACCESS": {
        "technique": "T1083",
        "name": "File and Directory Discovery",
        "tactic": "Discovery",
    },

    "FILE_ACCESS": {
        "technique": "T1005",
        "name": "Data from Local System",
        "tactic": "Collection",
    },

    "SENSITIVE_FILE_ACCESS": {
        "technique": "T1005",
        "name": "Data from Local System",
        "tactic": "Collection",
    },
}


def map_event(event_type: str):
    return MITRE_MAPPING.get(event_type)


def map_events(events: list):
    techniques = []

    for event in events:
        event_type = event.get("event_type")

        mapping = map_event(event_type)

        if mapping and mapping not in techniques:
            techniques.append(mapping)

    return techniques