# intelligence.py

from collections import Counter, defaultdict


HIT_RESULTS = {"1B", "2B", "3B", "HR"}
ON_BASE_RESULTS = {"1B", "2B", "3B", "HR", "BB", "HBP"}
OUT_RESULTS = {"GO", "FO", "LO", "PO", "FC", "GDP", "SAC", "SF"}
K_RESULTS = {"K Swinging", "K Looking"}


def iter_abs(lineup, chart_data, active_abs):
    for p_idx, player in enumerate(lineup):
        name = player.get("name") or f"Player {p_idx + 1}"

        for ab in range(1, active_abs + 1):
            data = chart_data.get(p_idx, {}).get(f"ab_{ab}", {})
            if any(data.get(k) for k in data if k != "batter"):
                yield p_idx, name, ab, data


def build_team_summary(lineup, chart_data, active_abs):
    abs_list = list(iter_abs(lineup, chart_data, active_abs))

    total = len(abs_list)
    hits = sum(1 for _, _, _, d in abs_list if d.get("result") in HIT_RESULTS)
    walks = sum(1 for _, _, _, d in abs_list if d.get("result") in {"BB", "HBP"})
    strikeouts = sum(1 for _, _, _, d in abs_list if d.get("result") in K_RESULTS)
    hard = sum(1 for _, _, _, d in abs_list if d.get("quality") in {"Hard Hit", "Barrel"})
    barrels = sum(1 for _, _, _, d in abs_list if d.get("quality") == "Barrel")
    chase = sum(1 for _, _, _, d in abs_list if "Chase" in str(d.get("zone", "")))

    pitch_counter = Counter(d.get("pitch") for _, _, _, d in abs_list if d.get("pitch"))
    zone_counter = Counter(d.get("zone") for _, _, _, d in abs_list if d.get("zone"))
    direction_counter = Counter(d.get("direction") for _, _, _, d in abs_list if d.get("direction"))
    quality_counter = Counter(d.get("quality") for _, _, _, d in abs_list if d.get("quality"))

    return {
        "total_abs": total,
        "hits": hits,
        "walks_hbp": walks,
        "strikeouts": strikeouts,
        "hard_contacts": hard,
        "barrels": barrels,
        "chase_events": chase,
        "top_pitch": pitch_counter.most_common(1)[0][0] if pitch_counter else "-",
        "top_zone": zone_counter.most_common(1)[0][0] if zone_counter else "-",
        "top_direction": direction_counter.most_common(1)[0][0] if direction_counter else "-",
        "quality_counter": quality_counter,
        "pitch_counter": pitch_counter,
        "zone_counter": zone_counter,
        "direction_counter": direction_counter,
    }


def build_player_summaries(lineup, chart_data, active_abs):
    players = defaultdict(list)

    for p_idx, name, ab, data in iter_abs(lineup, chart_data, active_abs):
        players[name].append(data)

    summaries = {}

    for name, abs_list in players.items():
        total = len(abs_list)
        hits = sum(1 for d in abs_list if d.get("result") in HIT_RESULTS)
        walks = sum(1 for d in abs_list if d.get("result") in {"BB", "HBP"})
        strikeouts = sum(1 for d in abs_list if d.get("result") in K_RESULTS)
        hard = sum(1 for d in abs_list if d.get("quality") in {"Hard Hit", "Barrel"})
        chase = sum(1 for d in abs_list if "Chase" in str(d.get("zone", "")))

        pitch_counter = Counter(d.get("pitch") for d in abs_list if d.get("pitch"))
        zone_counter = Counter(d.get("zone") for d in abs_list if d.get("zone"))
        direction_counter = Counter(d.get("direction") for d in abs_list if d.get("direction"))

        summaries[name] = {
            "PA": total,
            "H": hits,
            "BB_HBP": walks,
            "K": strikeouts,
            "Hard": hard,
            "Chase": chase,
            "Best Pitch": pitch_counter.most_common(1)[0][0] if pitch_counter else "-",
            "Common Zone": zone_counter.most_common(1)[0][0] if zone_counter else "-",
            "Main Direction": direction_counter.most_common(1)[0][0] if direction_counter else "-",
        }

    return summaries


def generate_game_observations(summary):
    observations = []

    total = summary["total_abs"]

    if total == 0:
        return ["No charted at-bats yet."]

    hard_rate = summary["hard_contacts"] / total
    chase_rate = summary["chase_events"] / total
    k_rate = summary["strikeouts"] / total

    if hard_rate >= 0.35:
        observations.append("The group produced strong contact quality overall.")
    elif hard_rate <= 0.15:
        observations.append("Contact quality was limited and should be reviewed.")

    if chase_rate >= 0.25:
        observations.append("The offense expanded the zone too often.")
    elif chase_rate <= 0.10:
        observations.append("The group showed solid strike-zone control.")

    if k_rate >= 0.30:
        observations.append("Strikeouts were elevated and may require approach review.")

    if summary["top_direction"] != "-":
        observations.append(f"Most charted contact went toward {summary['top_direction']}.")

    if summary["top_pitch"] != "-":
        observations.append(f"The most common finishing pitch was {summary['top_pitch']}.")

    return observations