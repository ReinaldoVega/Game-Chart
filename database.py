# database.py

import json
import os
from datetime import datetime

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "saved_games.json")


def ensure_data_file():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)


def load_games():
    ensure_data_file()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                return {}

            return json.loads(content)

    except json.JSONDecodeError:
        return {}


def save_games(games):
    ensure_data_file()

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=2)


def create_game_id(game_info):
    team = game_info.get("team", "team").replace(" ", "_")
    opponent = game_info.get("opponent", "opponent").replace(" ", "_")
    date = game_info.get("date", "")
    timestamp = datetime.now().strftime("%H%M%S")

    return f"{date}_{team}_vs_{opponent}_{timestamp}"


def save_game(game_info, lineup, chart_data, active_abs):
    games = load_games()

    game_id = game_info.get("game_id")

    if not game_id:
        game_id = create_game_id(game_info)
        game_info["game_id"] = game_id

    games[game_id] = {
        "game_id": game_id,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "game_info": game_info,
        "lineup": lineup,
        "chart_data": chart_data,
        "active_abs": active_abs,
    }

    save_games(games)

    return game_id


def delete_game(game_id):
    games = load_games()

    if game_id in games:
        del games[game_id]
        save_games(games)


def get_game(game_id):
    games = load_games()
    return games.get(game_id)