# workflow_engine.py

REQUIRED_BY_RESULT = {
    "BB": ["result", "pitch", "count", "zone"],
    "HBP": ["result", "pitch", "count", "zone"],
    "K Swinging": ["result", "pitch", "count", "zone"],
    "K Looking": ["result", "pitch", "count", "zone"],

    "1B": ["result", "pitch", "zone", "contact_type", "direction", "quality"],
    "2B": ["result", "pitch", "zone", "contact_type", "direction", "quality"],
    "3B": ["result", "pitch", "zone", "contact_type", "direction", "quality"],
    "HR": ["result", "pitch", "zone", "contact_type", "direction", "quality"],

    "GO": ["result", "pitch", "zone", "contact_type", "direction"],
    "FO": ["result", "pitch", "zone", "contact_type", "direction"],
    "LO": ["result", "pitch", "zone", "contact_type", "direction"],
    "PO": ["result", "pitch", "zone", "contact_type", "direction"],

    "ROE": ["result", "pitch", "zone", "contact_type", "direction"],
    "FC": ["result", "pitch", "zone", "contact_type", "direction"],
    "SAC": ["result", "pitch", "zone", "contact_type", "direction"],
    "SF": ["result", "pitch", "zone", "contact_type", "direction"],
    "GDP": ["result", "pitch", "zone", "contact_type", "direction"],
}


FIELD_LABELS = {
    "result": "Result",
    "pitch": "Pitch Type",
    "velo": "Pitch Velo",
    "count": "Count",
    "zone": "Pitch Zone",
    "contact_type": "Contact Type",
    "direction": "Field Direction",
    "quality": "Contact Quality",
    "situation": "Situation",
    "comment": "Comment",
}


def get_required_fields(ab_data):
    result = ab_data.get("result", "")

    if not result:
        return ["result"]

    return REQUIRED_BY_RESULT.get(
        result,
        ["result", "pitch", "zone"],
    )


def get_missing_fields(ab_data):
    required = get_required_fields(ab_data)

    missing = []

    for field in required:
        if not ab_data.get(field):
            missing.append(field)

    return missing


def get_completion_status(ab_data):
    missing = get_missing_fields(ab_data)
    required = get_required_fields(ab_data)

    total = len(required)
    completed = total - len(missing)

    if total == 0:
        pct = 100
    else:
        pct = int((completed / total) * 100)

    return {
        "required": required,
        "missing": missing,
        "completed": completed,
        "total": total,
        "pct": pct,
    }


def get_next_step(ab_data):
    missing = get_missing_fields(ab_data)

    if not missing:
        return "Done"

    return FIELD_LABELS.get(missing[0], missing[0])