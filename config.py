# config.py

APP_TITLE = "Tigers At-Bat Chart"

# ===========================
# App Settings
# ===========================

MAX_PLAYERS = 9
DEFAULT_ABS = 5
MAX_ABS = 9

LOGO_PATH = "assets/tigers_logo.webp"
EXPORTS_DIR = "exports"

# ===========================
# Colors
# ===========================

TIGERS_NAVY = "#0C2340"
TIGERS_ORANGE = "#FA4616"

DARK_BG = "#07111F"
PANEL_BG = "#0B1B2E"
CARD_DARK = "#102A44"
BORDER_DARK = "#1E3A5F"

TEXT_LIGHT = "#F8FAFC"
TEXT_MUTED = "#94A3B8"

SUCCESS = "#16A34A"
WARNING = "#F59E0B"
DANGER = "#DC2626"

# ===========================
# Options
# ===========================

POSITION_OPTIONS = [
    "",
    "C",
    "1B",
    "2B",
    "3B",
    "SS",
    "LF",
    "CF",
    "RF",
    "DH",
]

BATS_OPTIONS = [
    "",
    "R",
    "L",
    "S",
]

PLAYER_ROLE_OPTIONS = [
    "Starter",
    "PH",
    "Sub",
]

RESULT_OPTIONS = [
    "1B",
    "2B",
    "3B",
    "HR",
    "BB",
    "HBP",
    "K Swinging",
    "K Looking",
    "GO",
    "FO",
    "LO",
    "PO",
    "ROE",
    "FC",
    "SAC",
    "SF",
    "GDP",
    "Other",
]

PITCH_OPTIONS = [
    "FB",
    "SI",
    "CT",
    "SL",
    "SW",
    "CB",
    "CH",
    "SP",
    "Other",
]

COUNT_OPTIONS = [
    "0-0",
    "0-1",
    "0-2",
    "1-0",
    "1-1",
    "1-2",
    "2-0",
    "2-1",
    "2-2",
    "3-0",
    "3-1",
    "3-2",
]

CONTACT_TYPE_OPTIONS = [
    "GB",
    "LD",
    "FB",
    "PU",
    "Bunt",
]

CONTACT_QUALITY_OPTIONS = [
    "Barrel",
    "Hard Hit",
    "Solid",
    "Weak",
    "Soft",
]

DIRECTION_OPTIONS = [
    "P",
    "C",
    "1B",
    "2B",
    "3B",
    "SS",
    "LF",
    "CF",
    "RF",
]

SITUATION_OPTIONS = [
    "1st Pitch Swing",
    "2 Strike",
    "RISP",
    "Leadoff",
    "Sac Situation",
    "Hit & Run",
    "Runner Moving",
]