# workflow_engine.py

WORKFLOW_BY_RESULT = {
    "1B": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "2B": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "3B": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "HR": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],

    "BB": ["pitch", "count", "comment"],
    "HBP": ["pitch", "count", "comment"],

    "K Swinging": ["pitch", "zone", "count", "comment"],
    "K Looking": ["pitch", "zone", "count", "comment"],

    "GO": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "FO": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "LO": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "PO": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],

    "ROE": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "FC": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "SAC": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "SF": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "GDP": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    "Other": ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
}


FIELD_LABELS = {
    "result": "Result",
    "pitch": "Pitch Type",
    "velo": "Pitch Velo",
    "zone": "Pitch Location",
    "count": "Count",
    "direction": "Field Direction",
    "contact_type": "Contact Type",
    "quality": "Contact Quality",
    "situation": "Situation",
    "comment": "Comment",
}


def get_workflow_steps(result):
    if not result:
        return ["result"]

    return ["result"] + WORKFLOW_BY_RESULT.get(
        result,
        ["pitch", "zone", "direction", "contact_type", "quality", "comment"],
    )


def get_missing_required_fields(ab_data):
    result = ab_data.get("result", "")

    steps = get_workflow_steps(result)

    missing = []

    for field in steps:
        if field == "comment":
            continue

        if not ab_data.get(field, ""):
            missing.append(field)

    return missing


def get_next_step(ab_data):
    missing = get_missing_required_fields(ab_data)

    if missing:
        return missing[0]

    return "done"


def get_progress_text(ab_data):
    steps = get_workflow_steps(ab_data.get("result", ""))
    required_steps = [s for s in steps if s != "comment"]

    completed = 0

    for field in required_steps:
        if ab_data.get(field, ""):
            completed += 1

    total = len(required_steps)

    return f"{completed}/{total}"


def get_next_step_label(ab_data):
    next_step = get_next_step(ab_data)

    if next_step == "done":
        return "Complete"

    return FIELD_LABELS.get(next_step, next_step.title())