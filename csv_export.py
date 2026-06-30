# csv_export.py

import pandas as pd


def build_chart_dataframe(game_info, lineup, chart_data):
    rows = []

    for idx, player in enumerate(lineup):
        if not player.get("name"):
            continue

        row = {
            "Lineup": idx + 1,
            "Player": player.get("name", ""),
            "Position": player.get("position", ""),
        }

        for ab in range(1, 6):
            key = f"ab_{ab}"
            ab_data = chart_data.get(idx, {}).get(key, {})

            row[f"AB {ab} Result"] = ab_data.get("result", "")
            row[f"AB {ab} Comment"] = ab_data.get("comment", "")

        rows.append(row)

    df = pd.DataFrame(rows)

    for key, value in game_info.items():
        df[key] = value

    return df


def export_chart_csv(game_info, lineup, chart_data):
    df = build_chart_dataframe(game_info, lineup, chart_data)
    return df.to_csv(index=False).encode("utf-8")