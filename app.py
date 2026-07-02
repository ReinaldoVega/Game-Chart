# app.py

import streamlit as st
from datetime import date

from config import *
from csv_export import export_chart_csv
from pdf_export import export_chart_pdf

from database import load_games, save_game, delete_game, get_game


st.set_page_config(
    page_title="TigerVision Charting",
    page_icon="🐅",
    layout="wide",
)


def blank_ab():
    return {
        "batter": "Starter",
        "result": "",
        "pitch": "",
        "velo": "",
        "count": "",
        "zone": "",
        "contact_type": "",
        "direction": "",
        "quality": "",
        "situation": "",
        "comment": "",
    }
    
def new_game():
    for key in ["game_info", "lineup", "chart_data"]:
        if key in st.session_state:
            del st.session_state[key]

    st.session_state.active_abs = DEFAULT_ABS
    st.session_state.selected_player = 0
    st.session_state.selected_ab = 1
    st.session_state.screen = "chart"
    init_state()
    st.rerun()


def open_game(game_id):
    game = get_game(game_id)

    if game:
        st.session_state.game_info = game["game_info"]
        st.session_state.lineup = game["lineup"]
        st.session_state.chart_data = game["chart_data"]
        st.session_state.active_abs = game.get("active_abs", DEFAULT_ABS)
        st.session_state.selected_player = 0
        st.session_state.selected_ab = 1
        st.session_state.screen = "chart"
        st.rerun()


def save_current_game():
    game_id = save_game(
        st.session_state.game_info,
        st.session_state.lineup,
        st.session_state.chart_data,
        st.session_state.active_abs,
    )
    st.session_state.game_info["game_id"] = game_id
    st.success("Game saved.")


def init_state():
    st.session_state.setdefault("theme_mode", "Dark")
    st.session_state.setdefault("screen", "game_center")
    st.session_state.setdefault("active_abs", DEFAULT_ABS)
    st.session_state.setdefault("selected_player", 0)
    st.session_state.setdefault("selected_ab", 1)

    if "game_info" not in st.session_state:
        st.session_state.game_info = {
            "date": str(date.today()),
            "team": "DSL Tigers",
            "opponent": "",
            "home_away": "",
            "game_number": "",
            "innings": "",
            "score": "",
            "notes": "",
        }

    if "lineup" not in st.session_state:
        st.session_state.lineup = [
            {
                "name": "",
                "position": "",
                "bats": "",
                "subs": [],
            }
            for _ in range(MAX_PLAYERS)
        ]

    if "chart_data" not in st.session_state:
        st.session_state.chart_data = {}

    for p in range(MAX_PLAYERS):
        st.session_state.chart_data.setdefault(p, {})
        for ab in range(1, MAX_ABS + 1):
            st.session_state.chart_data[p].setdefault(f"ab_{ab}", blank_ab())


def css():
    theme = st.session_state.get("theme_mode", "Dark")

    if theme == "Light":
        bg = "#F5F7FA"
        bg_radial_1 = "rgba(250,70,22,.10)"
        bg_radial_2 = "rgba(12,35,64,.10)"
        panel = "rgba(255,255,255,.94)"
        card = "#FFFFFF"
        card_2 = "#F8FAFC"
        border = "rgba(12,35,64,.16)"
        text = "#0F172A"
        muted = "#475569"
        button_bg = "linear-gradient(180deg, #FFFFFF, #F1F5F9)"
        button_text = "#0C2340"
        input_bg = "#FFFFFF"
        input_text = "#0F172A"
        header_bg = "linear-gradient(135deg, rgba(255,255,255,.96), rgba(241,245,249,.96))"
        header_text = "#0C2340"
        header_sub = "#475569"
        shadow = "0 14px 30px rgba(15,23,42,.10)"
        filled_bg = "linear-gradient(180deg, rgba(250,70,22,.12), rgba(255,255,255,.98))"
    else:
        bg = "#07111F"
        bg_radial_1 = "rgba(250,70,22,.16)"
        bg_radial_2 = "rgba(12,35,64,.55)"
        panel = "rgba(11,27,46,.92)"
        card = "#102A44"
        card_2 = "#0B1B2E"
        border = "rgba(148,163,184,.18)"
        text = "#F8FAFC"
        muted = "#94A3B8"
        button_bg = "linear-gradient(180deg, #132F4F, #0B1B2E)"
        button_text = "#F8FAFC"
        input_bg = "#07111F"
        input_text = "#F8FAFC"
        header_bg = "linear-gradient(135deg, rgba(12,35,64,.98), rgba(7,17,31,.96))"
        header_text = "#FFFFFF"
        header_sub = "#CBD5E1"
        shadow = "0 20px 40px rgba(0,0,0,.28)"
        filled_bg = "linear-gradient(180deg, rgba(250,70,22,.16), rgba(16,42,68,.96))"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                radial-gradient(circle at top left, {bg_radial_1}, transparent 28%),
                radial-gradient(circle at top right, {bg_radial_2}, transparent 30%),
                {bg};
            color: {text};
        }}

        .main-header {{
            background: {header_bg};
            padding: 22px 28px;
            border-radius: 26px;
            border: 1px solid {border};
            border-left: 8px solid #FA4616;
            margin-bottom: 18px;
            box-shadow: {shadow};
        }}

        .main-header h1 {{
            color: {header_text};
            margin: 0;
            font-size: 32px;
            letter-spacing: .5px;
        }}

        .main-header p {{
            color: {header_sub};
            margin: 6px 0 0 0;
            font-size: 14px;
        }}

        .panel {{
            background: {panel};
            border: 1px solid {border};
            border-radius: 22px;
            padding: 18px;
            margin-bottom: 18px;
            box-shadow: {shadow};
            backdrop-filter: blur(10px);
        }}

        .section-title {{
            color: {text};
            font-weight: 900;
            font-size: 19px;
            margin-bottom: 12px;
            letter-spacing: .3px;
        }}

        .muted {{
            color: {muted};
            font-size: 12px;
        }}

        .chip {{
            display: inline-block;
            background: {card_2};
            color: {text};
            border: 1px solid {border};
            border-radius: 999px;
            padding: 4px 8px;
            margin: 2px;
            font-size: 11px;
            font-weight: 800;
        }}

        .ab-card {{
            background: linear-gradient(180deg, {card}, {card_2});
            border: 1px solid {border};
            border-radius: 20px;
            padding: 14px;
            min-height: 138px;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
        }}

        .ab-card-filled {{
            background: {filled_bg};
            border: 2px solid #FA4616;
            border-radius: 20px;
            padding: 14px;
            min-height: 138px;
            box-shadow: 0 0 22px rgba(250,70,22,.18);
        }}

        .ab-number {{
            color: {muted};
            font-size: 12px;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: .6px;
        }}

        .ab-result {{
            color: {text};
            font-size: 28px;
            font-weight: 1000;
            margin: 6px 0;
        }}

        div[data-testid="stButton"] button {{
            border-radius: 14px;
            font-weight: 900;
            border: 1px solid {border};
            background: {button_bg};
            color: {button_text};
            min-height: 42px;
            transition: all .15s ease-in-out;
        }}

        div[data-testid="stButton"] button:hover {{
            border-color: #FA4616;
            color: {button_text};
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(250,70,22,.18);
        }}

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {{
            background-color: {input_bg};
            color: {input_text};
            border: 1px solid {border};
            border-radius: 14px;
        }}

        div[data-testid="stSelectbox"] div {{
            border-radius: 14px;
            color: {input_text};
        }}

        div[data-testid="stTextArea"] textarea {{
            min-height: 98px;
            font-size: 13px;
        }}

        .stExpander {{
            border: 1px solid {border} !important;
            border-radius: 18px !important;
            overflow: hidden;
            background: {panel};
        }}

        hr {{
            border-color: {border};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def game_center():
    st.markdown(
        """
        <div class="main-header">
            <h1>🐅 TigerVision</h1>
            <p>Game Center — create, continue, and manage charted games.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Game Center</div>", unsafe_allow_html=True)

    if st.button("➕ New Game", use_container_width=True):
        new_game()

    st.markdown("</div>", unsafe_allow_html=True)

    games = load_games()

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Recent Games</div>", unsafe_allow_html=True)

    if not games:
        st.info("No saved games yet.")
    else:
        sorted_games = sorted(
            games.values(),
            key=lambda g: g.get("saved_at", ""),
            reverse=True,
        )

        for game in sorted_games:
            game_id = game["game_id"]
            info = game["game_info"]

            team = info.get("team", "Team")
            opponent = info.get("opponent", "Opponent")
            date_txt = info.get("date", "")
            game_number = info.get("game_number", "")
            saved_at = game.get("saved_at", "")

            c1, c2, c3 = st.columns([3, 1, 1])

            with c1:
                st.markdown(
                    f"""
                    <div class="ab-card">
                        <div class="ab-number">{date_txt} • Game {game_number}</div>
                        <div class="ab-result" style="font-size:20px;">{team} vs {opponent}</div>
                        <div class="muted">Last saved: {saved_at}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with c2:
                if st.button("Continue", key=f"open_{game_id}", use_container_width=True):
                    open_game(game_id)

            with c3:
                if st.button("Delete", key=f"delete_{game_id}", use_container_width=True):
                    delete_game(game_id)
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def theme_toggle():
    c1, c2, c3 = st.columns([6, 1, 1])

    with c2:
        if st.button("🌙 Dark", use_container_width=True):
            st.session_state.theme_mode = "Dark"
            st.rerun()

    with c3:
        if st.button("☀️ Light", use_container_width=True):
            st.session_state.theme_mode = "Light"
            st.rerun()

def header():
    info = st.session_state.game_info

    date_txt = info.get("date", "")
    team = info.get("team", "DSL Tigers") or "DSL Tigers"
    opponent = info.get("opponent", "") or "Opponent"
    home_away = info.get("home_away", "") or "-"
    game_number = info.get("game_number", "") or "-"
    inning = info.get("inning", "") or "-"
    score = info.get("score", "") or "-"

    st.markdown("<div class='main-header'>", unsafe_allow_html=True)

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown(
            """
            <div style="font-size:13px;color:#94A3B8;font-weight:800;letter-spacing:1.8px;">
                PROFESSIONAL GAME CHARTING
            </div>
            <h1>🐅 TigerVision</h1>
            <p>Player Development Charting System</p>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div style="text-align:right;">
                <div style="font-size:18px;font-weight:900;color:white;">
                    {team} vs {opponent}
                </div>
                <div style="margin-top:8px;">
                    <span class="chip">📅 {date_txt}</span>
                    <span class="chip">🏟️ {home_away}</span>
                    <span class="chip">⚾ Game {game_number}</span>
                    <span class="chip">⏱️ {inning}</span>
                    <span class="chip">📊 {score}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def game_info_panel():
    with st.expander("Game Info", expanded=False):
        c1, c2, c3, c4, c5, c6, c7 = st.columns([1, 1.1, 1.3, .8, .8, .8, .8])

        with c1:
            game_date = st.date_input(
                "Date",
                value=date.fromisoformat(st.session_state.game_info["date"]),
            )
            st.session_state.game_info["date"] = str(game_date)

        with c2:
            st.session_state.game_info["team"] = st.text_input(
                "Team",
                value=st.session_state.game_info["team"],
            )

        with c3:
            st.session_state.game_info["opponent"] = st.text_input(
                "Opponent",
                value=st.session_state.game_info["opponent"],
            )

        with c4:
            st.session_state.game_info["home_away"] = st.selectbox(
                "H/A",
                ["", "Home", "Away"],
                index=["", "Home", "Away"].index(st.session_state.game_info.get("home_away", "")),
            )

        with c5:
            st.session_state.game_info["game_number"] = st.text_input(
                "Game #",
                value=st.session_state.game_info["game_number"],
            )

        with c6:
            st.session_state.game_info["inning"] = st.text_input(
                "Inning",
                value=st.session_state.game_info.get("inning", ""),
            )

        with c7:
            st.session_state.game_info["score"] = st.text_input(
                "Score",
                value=st.session_state.game_info.get("score", ""),
            )

        st.session_state.game_info["notes"] = st.text_area(
            "General Notes",
            value=st.session_state.game_info["notes"],
            placeholder="General notes...",
        )


def lineup_panel():
    with st.expander("Lineup / PH / Subs", expanded=True):
        for i in range(MAX_PLAYERS):
            st.markdown(f"#### Spot {i + 1}")

            c1, c2, c3 = st.columns([2.4, 1, 1])

            with c1:
                st.session_state.lineup[i]["name"] = st.text_input(
                    "Starter",
                    value=st.session_state.lineup[i]["name"],
                    key=f"starter_{i}",
                    placeholder="Player name",
                )

            with c2:
                current_pos = st.session_state.lineup[i].get("position", "")
                st.session_state.lineup[i]["position"] = st.selectbox(
                    "POS",
                    POSITION_OPTIONS,
                    index=POSITION_OPTIONS.index(current_pos) if current_pos in POSITION_OPTIONS else 0,
                    key=f"pos_{i}",
                )

            with c3:
                current_bats = st.session_state.lineup[i].get("bats", "")
                st.session_state.lineup[i]["bats"] = st.selectbox(
                    "Bats",
                    BATS_OPTIONS,
                    index=BATS_OPTIONS.index(current_bats) if current_bats in BATS_OPTIONS else 0,
                    key=f"bats_{i}",
                )

            c_add, c_space = st.columns([1, 4])
            with c_add:
                if st.button("+ PH/Sub", key=f"add_sub_{i}", use_container_width=True):
                    st.session_state.lineup[i]["subs"].append(
                        {
                            "name": "",
                            "role": "PH",
                            "inning": "",
                            "position": "",
                        }
                    )
                    st.rerun()

            for s_idx, sub in enumerate(st.session_state.lineup[i]["subs"]):
                sc1, sc2, sc3, sc4, sc5 = st.columns([2, .9, .8, .9, .6])

                with sc1:
                    sub["name"] = st.text_input(
                        "Name",
                        value=sub.get("name", ""),
                        key=f"sub_name_{i}_{s_idx}",
                        placeholder="Sub name",
                    )

                with sc2:
                    sub["role"] = st.selectbox(
                        "Role",
                        PLAYER_ROLE_OPTIONS,
                        index=PLAYER_ROLE_OPTIONS.index(sub.get("role", "PH"))
                        if sub.get("role", "PH") in PLAYER_ROLE_OPTIONS
                        else 0,
                        key=f"sub_role_{i}_{s_idx}",
                    )

                with sc3:
                    sub["inning"] = st.text_input(
                        "Inn",
                        value=sub.get("inning", ""),
                        key=f"sub_inn_{i}_{s_idx}",
                    )

                with sc4:
                    sub["position"] = st.selectbox(
                        "POS",
                        POSITION_OPTIONS,
                        index=POSITION_OPTIONS.index(sub.get("position", ""))
                        if sub.get("position", "") in POSITION_OPTIONS
                        else 0,
                        key=f"sub_pos_{i}_{s_idx}",
                    )

                with sc5:
                    if st.button("X", key=f"remove_sub_{i}_{s_idx}", use_container_width=True):
                        st.session_state.lineup[i]["subs"].pop(s_idx)
                        st.rerun()

            st.divider()


def player_picker():
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Lineup</div>", unsafe_allow_html=True)

    for i, player in enumerate(st.session_state.lineup):
        name = player.get("name", "").strip() or f"Player {i + 1}"
        pos = player.get("position", "")
        bats = player.get("bats", "")

        label = f"{i + 1}. {name}"
        if pos:
            label += f" | {pos}"
        if bats:
            label += f" | {bats}"

        if st.button(label, key=f"pick_player_{i}", use_container_width=True):
            st.session_state.selected_player = i
            st.rerun()

        for sub in player.get("subs", []):
            if sub.get("name"):
                st.markdown(
                    f"<div class='muted'>↳ {sub.get('role')} {sub.get('name')} "
                    f"{sub.get('position', '')} Inn: {sub.get('inning', '')}</div>",
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)


def ab_picker():
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>At-Bats</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("+ Add AB", use_container_width=True):
            if st.session_state.active_abs < MAX_ABS:
                st.session_state.active_abs += 1
                st.rerun()

    with c2:
        if st.button("- Remove AB", use_container_width=True):
            if st.session_state.active_abs > DEFAULT_ABS:
                st.session_state.active_abs -= 1
                if st.session_state.selected_ab > st.session_state.active_abs:
                    st.session_state.selected_ab = st.session_state.active_abs
                st.rerun()

    for ab in range(1, st.session_state.active_abs + 1):
        data = st.session_state.chart_data[st.session_state.selected_player][f"ab_{ab}"]
        label = f"AB {ab}"
        if data.get("result"):
            label += f" | {data.get('result')}"

        if st.button(label, key=f"pick_ab_{ab}", use_container_width=True):
            st.session_state.selected_ab = ab
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def button_group(title, options, field, p, ab, cols_count=4):
    st.markdown(f"**{title}**")
    key = f"ab_{ab}"
    current = st.session_state.chart_data[p][key].get(field, "")

    for start in range(0, len(options), cols_count):
        row = options[start:start + cols_count]
        cols = st.columns(len(row))

        for col, opt in zip(cols, row):
            selected = current == opt
            label = f"✅ {opt}" if selected else opt

            if col.button(label, key=f"{field}_{p}_{ab}_{opt}", use_container_width=True):
                st.session_state.chart_data[p][key][field] = opt
                st.rerun()


def ab_cards():
    p = st.session_state.selected_player
    player = st.session_state.lineup[p]
    name = player.get("name", "").strip() or f"Player {p + 1}"

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{p + 1}. {name} — AB Summary</div>", unsafe_allow_html=True)

    cols = st.columns(st.session_state.active_abs)

    for ab in range(1, st.session_state.active_abs + 1):
        data = st.session_state.chart_data[p][f"ab_{ab}"]
        filled = any(data.get(k) for k in data if k != "batter")
        card_class = "ab-card-filled" if filled else "ab-card"

        with cols[ab - 1]:
            st.markdown(
                f"""
                <div class="{card_class}">
                    <div class="ab-number">AB {ab}</div>
                    <div class="ab-result">{data.get("result") or "-"}</div>
                    <div class="muted">Batter: {data.get("batter", "Starter")}</div>
                    <div class="muted">Pitch: {data.get("pitch", "")} {data.get("velo", "")}</div>
                    <div class="muted">Count: {data.get("count", "")}</div>
                    <div class="muted">Zone: {data.get("zone", "")}</div>
                    <div class="muted">Contact: {data.get("contact_type", "")} {data.get("direction", "")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


def chart_editor():
    p = st.session_state.selected_player
    ab = st.session_state.selected_ab
    key = f"ab_{ab}"
    data = st.session_state.chart_data[p][key]
    player = st.session_state.lineup[p]

    starter_name = player.get("name", "").strip() or f"Player {p + 1}"
    subs = [s for s in player.get("subs", []) if s.get("name")]

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='section-title'>Chart Editor — {starter_name} | AB {ab}</div>",
        unsafe_allow_html=True,
    )

    batter_options = ["Starter"] + [f"{s.get('role')} - {s.get('name')}" for s in subs]

    data["batter"] = st.selectbox(
        "Who took this AB?",
        batter_options,
        index=batter_options.index(data.get("batter", "Starter"))
        if data.get("batter", "Starter") in batter_options
        else 0,
        key=f"batter_{p}_{ab}",
    )

    c1, c2 = st.columns([1, 1])

    with c1:
        button_group("Result", RESULT_OPTIONS, "result", p, ab, 4)
        button_group("Pitch Type", PITCH_OPTIONS, "pitch", p, ab, 4)

        data["velo"] = st.text_input(
            "Pitch Velo",
            value=data.get("velo", ""),
            key=f"velo_{p}_{ab}",
            placeholder="Example: 94.5",
        )

        button_group("Count", COUNT_OPTIONS, "count", p, ab, 4)

    with c2:
        button_group("Strike Zone", ["1", "2", "3", "4", "5", "6", "7", "8", "9"], "zone", p, ab, 3)
        button_group("Chase Zone", ["Chase Up", "Chase Down", "Chase In", "Chase Away"], "zone", p, ab, 2)
        button_group("Contact Type", CONTACT_TYPE_OPTIONS, "contact_type", p, ab, 5)
        button_group("Direction", DIRECTION_OPTIONS, "direction", p, ab, 3)
        button_group("Quality", CONTACT_QUALITY_OPTIONS, "quality", p, ab, 3)

    button_group("Situation", SITUATION_OPTIONS, "situation", p, ab, 4)

    data["comment"] = st.text_area(
        "Comment",
        value=data.get("comment", ""),
        key=f"comment_{p}_{ab}",
        placeholder="Example: Hard LD to CF off FB middle-middle. Good swing decision.",
    )

    c_clear, c_next = st.columns(2)

    with c_clear:
        if st.button("Clear This AB", use_container_width=True):
            st.session_state.chart_data[p][key] = blank_ab()
            st.rerun()

    with c_next:
        if st.button("Save & Next AB", use_container_width=True):
            if st.session_state.selected_ab < st.session_state.active_abs:
                st.session_state.selected_ab += 1
            elif st.session_state.active_abs < MAX_ABS:
                st.session_state.active_abs += 1
                st.session_state.selected_ab += 1
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def exports_panel():
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Export</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            "Download CSV",
            data=export_chart_csv(
                st.session_state.game_info,
                st.session_state.lineup,
                st.session_state.chart_data,
            ),
            file_name="tiger_vision-chart.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with c2:
        st.download_button(
            "Download PDF",
            data=export_chart_pdf(
                st.session_state.game_info,
                st.session_state.lineup,
                st.session_state.chart_data,
            ),
            file_name="tiger_vision-chart.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


init_state()
css()
theme_toggle()

if st.session_state.screen == "game_center":
    game_center()
else:
    header()

    top1, top2, top3 = st.columns([1, 1, 1])

    with top1:
        if st.button("⬅️ Game Center", use_container_width=True):
            st.session_state.screen = "game_center"
            st.rerun()

    with top2:
        if st.button("💾 Save Game", use_container_width=True):
            save_current_game()

    with top3:
        if st.button("➕ New Game", use_container_width=True):
            new_game()

    game_info_panel()
    lineup_panel()

    left, right = st.columns([1.1, 2.9])

    with left:
        player_picker()
        ab_picker()

    with right:
        ab_cards()
        chart_editor()

    exports_panel()