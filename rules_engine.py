# rules_engine.py

NO_CONTACT_FIELDS = [
    "contact_type",
    "direction",
    "quality",
]

BALL_IN_PLAY_RESULTS = [
    "1B",
    "2B",
    "3B",
    "HR",
    "GO",
    "FO",
    "LO",
    "PO",
    "ROE",
    "FC",
    "SAC",
    "SF",
    "GDP",
]

HIT_RESULTS = ["1B", "2B", "3B", "HR"]

WALK_RESULTS = ["BB", "HBP"]

STRIKEOUT_RESULTS = ["K Swinging", "K Looking"]


RESULT_RULES = {
    "BB": {
        "clear": NO_CONTACT_FIELDS,
        "suggestions": {},
        "requires_contact": False,
        "note": "Walk. Contact fields cleared.",
    },

    "HBP": {
        "clear": NO_CONTACT_FIELDS,
        "suggestions": {},
        "requires_contact": False,
        "note": "Hit by pitch. Contact fields cleared.",
    },

    "K Swinging": {
        "clear": ["direction", "quality"],
        "suggestions": {
            "contact_type": "Swing & Miss",
        },
        "requires_contact": False,
        "note": "Swinging strikeout.",
    },

    "K Looking": {
        "clear": NO_CONTACT_FIELDS,
        "suggestions": {},
        "requires_contact": False,
        "note": "Looking strikeout.",
    },

    "HR": {
        "clear": [],
        "suggestions": {
            "contact_type": "FB",
            "quality": "Barrel",
        },
        "requires_contact": True,
        "note": "Home run. Barrel/Fly Ball suggested.",
    },

    "1B": {
        "clear": [],
        "suggestions": {},
        "requires_contact": True,
        "note": "Single.",
    },

    "2B": {
        "clear": [],
        "suggestions": {},
        "requires_contact": True,
        "note": "Double.",
    },

    "3B": {
        "clear": [],
        "suggestions": {},
        "requires_contact": True,
        "note": "Triple.",
    },

    "GO": {
        "clear": [],
        "suggestions": {
            "contact_type": "GB",
        },
        "requires_contact": True,
        "note": "Ground out. Ground Ball suggested.",
    },

    "FO": {
        "clear": [],
        "suggestions": {
            "contact_type": "FB",
        },
        "requires_contact": True,
        "note": "Fly out. Fly Ball suggested.",
    },

    "LO": {
        "clear": [],
        "suggestions": {
            "contact_type": "LD",
        },
        "requires_contact": True,
        "note": "Line out. Line Drive suggested.",
    },

    "PO": {
        "clear": [],
        "suggestions": {
            "contact_type": "PU",
        },
        "requires_contact": True,
        "note": "Pop out. Pop Up suggested.",
    },

    "SAC": {
        "clear": [],
        "suggestions": {
            "contact_type": "Bunt",
        },
        "requires_contact": True,
        "note": "Sacrifice bunt.",
    },

    "SF": {
        "clear": [],
        "suggestions": {
            "contact_type": "FB",
        },
        "requires_contact": True,
        "note": "Sacrifice fly.",
    },

    "GDP": {
        "clear": [],
        "suggestions": {
            "contact_type": "GB",
        },
        "requires_contact": True,
        "note": "Grounded into double play.",
    },
}


def apply_result_rules(ab_data):
    """
    Applies automatic baseball logic to the selected AB.

    Example:
    BB clears contact fields.
    HR suggests Barrel and FB.
    GO suggests GB.
    """

    result = ab_data.get("result", "")

    if not result:
        return ab_data, ""

    rule = RESULT_RULES.get(result)

    if not rule:
        return ab_data, ""

    # Clear fields that do not apply
    for field in rule.get("clear", []):
        ab_data[field] = ""

    # Apply suggestions only if field is empty
    for field, value in rule.get("suggestions", {}).items():
        if not ab_data.get(field):
            ab_data[field] = value

    return ab_data, rule.get("note", "")


def contact_fields_should_show(result):
    """
    Determines if contact fields should appear in the UI.
    """

    if result in WALK_RESULTS:
        return False

    if result in STRIKEOUT_RESULTS:
        return False

    return True


def get_result_category(result):
    """
    Used later for colors, reports, and cards.
    """

    if result in HIT_RESULTS:
        return "hit"

    if result == "HR":
        return "hr"

    if result in WALK_RESULTS:
        return "walk"

    if result in STRIKEOUT_RESULTS:
        return "strikeout"

    if result:
        return "out"

    return "empty"