# app.py

import streamlit as st
from datetime import date

from config import *
from csv_export import export_chart_csv
from pdf_export import export_chart_pdf
from database import load_games, save_game, delete_game, get_game
from rules_engine import apply_result_rules, contact_fields_should_show

st.set_page_config(
    page_title="TigerVision",
    page_icon="🐅",
    layout="wide",
)


# =========================
# STATE
# =========================

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


def init_state():
    st.session_state.setdefault("screen", "game_center")
    st.session_state.setdefault("theme_mode", "Dark")
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
            "inning": "",
            "score": "",
            "notes": "",
        }

    if "lineup" not in st.session_state:
        st.session_state.lineup = [
            {"name": "", "position": "", "bats": "", "subs": []}
            for _ in range(MAX_PLAYERS)
        ]

    if "chart_data" not in st.session_state:
        st.session_state.chart_data = {}

    for p in range(MAX_PLAYERS):
        st.session_state.chart_data.setdefault(p, {})
        for ab in range(1, MAX_ABS + 1):
            st.session_state.chart_data[p].setdefault(f"ab_{ab}", blank_ab())


# =========================
# SAVE / LOAD
# =========================

def save_current_game(show_message=True):
    game_id = save_game(
        st.session_state.game_info,
        st.session_state.lineup,
        st.session_state.chart_data,
        st.session_state.active_abs,
    )
    st.session_state.game_info["game_id"] = game_id

    if show_message:
        st.success("Game saved.")


def autosave():
    if st.session_state.get("game_info", {}).get("game_id"):
        save_current_game(show_message=False)


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


# =========================
# THEME
# =========================

def css():
    theme = st.session_state.get("theme_mode", "Dark")

    if theme == "Light":
        bg = "#F5F7FA"
        panel = "rgba(255,255,255,.96)"
        card = "#FFFFFF"
        card2 = "#F8FAFC"
        border = "rgba(12,35,64,.16)"
        text = "#0F172A"
        muted = "#475569"
        header = "linear-gradient(135deg, rgba(255,255,255,.98), rgba(241,245,249,.96))"
        button = "linear-gradient(180deg,#FFFFFF,#F1F5F9)"
        button_text = "#0C2340"
        input_bg = "#FFFFFF"
        shadow = "0 14px 30px rgba(15,23,42,.10)"
    else:
        bg = "#07111F"
        panel = "rgba(11,27,46,.94)"
        card = "#102A44"
        card2 = "#0B1B2E"
        border = "rgba(148,163,184,.18)"
        text = "#F8FAFC"
        muted = "#94A3B8"
        header = "linear-gradient(135deg, rgba(12,35,64,.98), rgba(7,17,31,.96))"
        button = "linear-gradient(180deg,#132F4F,#0B1B2E)"
        button_text = "#F8FAFC"
        input_bg = "#07111F"
        shadow = "0 20px 40px rgba(0,0,0,.28)"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                radial-gradient(circle at top left, rgba(250,70,22,.14), transparent 28%),
                radial-gradient(circle at top right, rgba(12,35,64,.25), transparent 30%),
                {bg};
            color: {text};
        }}

        .main-header {{
            background: {header};
            padding: 22px 28px;
            border-radius: 26px;
            border: 1px solid {border};
            border-left: 8px solid #FA4616;
            margin-bottom: 18px;
            box-shadow: {shadow};
        }}

        .main-header h1 {{
            color: {text};
            margin: 0;
            font-size: 34px;
            letter-spacing: .5px;
        }}

        .main-header p {{
            color: {muted};
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
        }}

        .section-title {{
            color: {text};
            font-weight: 900;
            font-size: 19px;
            margin-bottom: 12px;
        }}

        .muted {{
            color: {muted};
            font-size: 12px;
        }}

        .chip {{
            display:inline-block;
            background:{card2};
            color:{text};
            border:1px solid {border};
            border-radius:999px;
            padding:5px 9px;
            margin:2px;
            font-size:11px;
            font-weight:800;
        }}

        .ab-card {{
            background: linear-gradient(180deg,{card},{card2});
            border: 1px solid {border};
            border-radius: 20px;
            padding: 14px;
            min-height: 130px;
        }}

        .ab-card-filled {{
            background: linear-gradient(180deg,rgba(250,70,22,.16),{card});
            border: 2px solid #FA4616;
            border-radius: 20px;
            padding: 14px;
            min-height: 130px;
            box-shadow:0 0 22px rgba(250,70,22,.18);
        }}

        .ab-number {{
            color:{muted};
            font-size:12px;
            font-weight:900;
            letter-spacing:.6px;
        }}

        .ab-result {{
            color:{text};
            font-size:28px;
            font-weight:1000;
            margin:6px 0;
        }}

        div[data-testid="stButton"] button {{
            border-radius:14px;
            font-weight:900;
            border:1px solid {border};
            background:{button};
            color:{button_text};
            min-height:42px;
        }}

        div[data-testid="stButton"] button:hover {{
            border-color:#FA4616;
            transform:translateY(-1px);
            box-shadow:0 8px 18px rgba(250,70,22,.18);
        }}

        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {{
            background:{input_bg};
            color:{text};
            border:1px solid {border};
            border-radius:14px;
        }}

        div[data-testid="stTextArea"] textarea {{
            min-height:95px;
            font-size:13px;
        }}

        .stExpander {{
            border:1px solid {border} !important;
            border-radius:18px !important;
            overflow:hidden;
            background:{panel};
        }}

        hr {{
            border-color:{border};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


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


# =========================
# UI HELPERS
# =========================

def styled_label(field, opt, selected=False):
    prefix = ""

    if field == "result":
        if opt in ["1B", "2B", "3B"]:
            prefix = "🟢"
        elif opt == "HR":
            prefix = "🟠"
        elif opt in ["BB", "HBP"]:
            prefix = "🔵"
        elif "K" in opt:
            prefix = "🔴"
        else:
            prefix = "⚫"
    elif field == "pitch":
        prefix = "🟣"
    elif field == "zone":
        prefix = "🟧"
    elif field == "quality":
        prefix = "🟢" if opt in ["Barrel", "Hard Hit"] else "🟡" if opt == "Solid" else "🔴"
    elif field == "direction":
        prefix = "➡️"
    elif field == "contact_type":
        prefix = "⚾"
    elif field == "count":
        prefix = "🔢"
    elif field == "situation":
        prefix = "📌"

    label = f"{prefix} {opt}".strip()
    return f"✅ {label}" if selected else label


def button_group(title, options, field, p, ab, cols_count=4):
    if title:
        st.markdown(f"**{title}**")

    key = f"ab_{ab}"
    current = st.session_state.chart_data[p][key].get(field, "")

    for start in range(0, len(options), cols_count):
        row = options[start:start + cols_count]
        cols = st.columns(len(row))

        for col, opt in zip(cols, row):
            selected = current == opt
            label = styled_label(field, opt, selected)

            with col:
                if st.button(label, key=f"{field}_{p}_{ab}_{opt}", use_container_width=True):
                    st.session_state.chart_data[p][key][field] = opt

                    if field == "result":
                      st.session_state.chart_data[p][key], note = apply_result_rules(
                         st.session_state.chart_data[p][key]
                    )
                    if note:
                      st.toast(note)

            autosave()
            st.rerun()


def result_dot(result):
    if result in ["1B", "2B", "3B"]:
        return "🟢"
    if result == "HR":
        return "🟠"
    if result in ["BB", "HBP"]:
        return "🔵"
    if "K" in result:
        return "🔴"
    if result:
        return "⚫"
    return "⚪"


# =========================
# GAME CENTER
# =========================

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
        sorted_games = sorted(games.values(), key=lambda g: g.get("saved_at", ""), reverse=True)

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
                        <div class="ab-result" style="font-size:22px;">{team} vs {opponent}</div>
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


# =========================
# HEADER
# =========================

def header():
    info = st.session_state.game_info

    team = info.get("team", "DSL Tigers") or "DSL Tigers"
    opponent = info.get("opponent", "") or "Opponent"
    date_txt = info.get("date", "")
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
            <p>Quick Chart Mode</p>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div style="text-align:right;">
                <div style="font-size:19px;font-weight:900;">
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


# =========================
# GAME INFO / LINEUP
# =========================

def game_info_panel():
    with st.expander("Game Info", expanded=False):
        c1, c2, c3, c4, c5, c6, c7 = st.columns([1, 1.1, 1.3, .8, .8, .8, .8])

        with c1:
            d = st.date_input("Date", value=date.fromisoformat(st.session_state.game_info["date"]))
            st.session_state.game_info["date"] = str(d)

        with c2:
            st.session_state.game_info["team"] = st.text_input("Team", st.session_state.game_info["team"])

        with c3:
            st.session_state.game_info["opponent"] = st.text_input("Opponent", st.session_state.game_info["opponent"])

        with c4:
            opts = ["", "Home", "Away"]
            st.session_state.game_info["home_away"] = st.selectbox(
                "H/A",
                opts,
                index=opts.index(st.session_state.game_info.get("home_away", "")),
            )

        with c5:
            st.session_state.game_info["game_number"] = st.text_input("Game #", st.session_state.game_info["game_number"])

        with c6:
            st.session_state.game_info["inning"] = st.text_input("Inning", st.session_state.game_info.get("inning", ""))

        with c7:
            st.session_state.game_info["score"] = st.text_input("Score", st.session_state.game_info.get("score", ""))

        st.session_state.game_info["notes"] = st.text_area("General Notes", st.session_state.game_info["notes"])


def lineup_panel():
    with st.expander("Lineup / PH / Subs", expanded=False):
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

            if st.button("+ PH/Sub", key=f"add_sub_{i}", use_container_width=True):
                st.session_state.lineup[i]["subs"].append(
                    {"name": "", "role": "PH", "inning": "", "position": ""}
                )
                st.rerun()

            for s_idx, sub in enumerate(st.session_state.lineup[i]["subs"]):
                sc1, sc2, sc3, sc4, sc5 = st.columns([2, .9, .8, .9, .6])

                with sc1:
                    sub["name"] = st.text_input("Name", value=sub.get("name", ""), key=f"sub_name_{i}_{s_idx}")

                with sc2:
                    sub["role"] = st.selectbox(
                        "Role",
                        PLAYER_ROLE_OPTIONS,
                        index=PLAYER_ROLE_OPTIONS.index(sub.get("role", "PH"))
                        if sub.get("role", "PH") in PLAYER_ROLE_OPTIONS else 0,
                        key=f"sub_role_{i}_{s_idx}",
                    )

                with sc3:
                    sub["inning"] = st.text_input("Inn", value=sub.get("inning", ""), key=f"sub_inn_{i}_{s_idx}")

                with sc4:
                    sub["position"] = st.selectbox(
                        "POS",
                        POSITION_OPTIONS,
                        index=POSITION_OPTIONS.index(sub.get("position", ""))
                        if sub.get("position", "") in POSITION_OPTIONS else 0,
                        key=f"sub_pos_{i}_{s_idx}",
                    )

                with sc5:
                    if st.button("X", key=f"remove_sub_{i}_{s_idx}", use_container_width=True):
                        st.session_state.lineup[i]["subs"].pop(s_idx)
                        st.rerun()

            st.divider()


# =========================
# QUICK CHART
# =========================

def lineup_quick_panel():
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Lineup</div>", unsafe_allow_html=True)

    for i, player in enumerate(st.session_state.lineup):
        name = player.get("name", "").strip() or f"Player {i + 1}"
        pos = player.get("position", "")
        bats = player.get("bats", "")

        dots = ""
        for ab in range(1, st.session_state.active_abs + 1):
            r = st.session_state.chart_data[i][f"ab_{ab}"].get("result", "")
            dots += result_dot(r)

        label = f"{i + 1}. {name}"
        if pos:
            label += f" | {pos}"
        if bats:
            label += f" | {bats}"

        if st.button(label, key=f"pick_player_{i}", use_container_width=True):
            st.session_state.selected_player = i
            st.rerun()

        st.markdown(f"<div class='muted'>{dots}</div>", unsafe_allow_html=True)

        for sub in player.get("subs", []):
            if sub.get("name"):
                st.markdown(
                    f"<div class='muted'>↳ {sub.get('role')} {sub.get('name')} {sub.get('position','')} Inn {sub.get('inning','')}</div>",
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)


def ab_timeline():
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>At-Bats</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("+ Add AB", use_container_width=True):
            if st.session_state.active_abs < MAX_ABS:
                st.session_state.active_abs += 1
                autosave()
                st.rerun()

    with c2:
        if st.button("- Remove AB", use_container_width=True):
            if st.session_state.active_abs > DEFAULT_ABS:
                st.session_state.active_abs -= 1
                autosave()
                st.rerun()

    p = st.session_state.selected_player

    for ab in range(1, st.session_state.active_abs + 1):
        data = st.session_state.chart_data[p][f"ab_{ab}"]
        label = f"AB {ab} {result_dot(data.get('result',''))}"
        if data.get("result"):
            label += f" {data.get('result')}"

        if st.button(label, key=f"pick_ab_{ab}", use_container_width=True):
            st.session_state.selected_ab = ab
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def strike_zone_visual(p, ab):
    st.markdown("**🎯 Strike Zone**")

    zones = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

    for row in zones:
        cols = st.columns(3)
        for col, zone in zip(cols, row):
            with col:
                button_group("", [zone], "zone", p, ab, 1)

    st.markdown("**Chase**")
    c1, c2 = st.columns(2)

    with c1:
        button_group("", ["Chase Up", "Chase In"], "zone", p, ab, 1)

    with c2:
        button_group("", ["Chase Down", "Chase Away"], "zone", p, ab, 1)


def field_direction_visual(p, ab):
    st.markdown("**🧤 Field Direction**")

    row1 = st.columns(3)
    with row1[0]:
        button_group("", ["LF"], "direction", p, ab, 1)
    with row1[1]:
        button_group("", ["CF"], "direction", p, ab, 1)
    with row1[2]:
        button_group("", ["RF"], "direction", p, ab, 1)

    row2 = st.columns(4)
    with row2[0]:
        button_group("", ["3B"], "direction", p, ab, 1)
    with row2[1]:
        button_group("", ["SS"], "direction", p, ab, 1)
    with row2[2]:
        button_group("", ["2B"], "direction", p, ab, 1)
    with row2[3]:
        button_group("", ["1B"], "direction", p, ab, 1)

    row3 = st.columns(2)
    with row3[0]:
        button_group("", ["P"], "direction", p, ab, 1)
    with row3[1]:
        button_group("", ["C"], "direction", p, ab, 1)


def quick_chart_panel():
    p = st.session_state.selected_player
    ab = st.session_state.selected_ab
    data = st.session_state.chart_data[p][f"ab_{ab}"]

    player = st.session_state.lineup[p]
    name = player.get("name", "").strip() or f"Player {p + 1}"
    subs = [s for s in player.get("subs", []) if s.get("name")]

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>Quick Chart — {p + 1}. {name} | AB {ab}</div>", unsafe_allow_html=True)

    batter_options = ["Starter"] + [f"{s.get('role')} - {s.get('name')}" for s in subs]

    data["batter"] = st.selectbox(
        "Who took this AB?",
        batter_options,
        index=batter_options.index(data.get("batter", "Starter"))
        if data.get("batter", "Starter") in batter_options else 0,
        key=f"batter_{p}_{ab}",
    )

    left, right = st.columns([1.1, 1])

    with left:
        button_group("🟢 Result", RESULT_OPTIONS, "result", p, ab, 4)
        button_group("🟣 Pitch", PITCH_OPTIONS, "pitch", p, ab, 4)

        data["velo"] = st.text_input(
            "Pitch Velo",
            value=data.get("velo", ""),
            key=f"velo_{p}_{ab}",
            placeholder="94.5",
        )

        button_group("🔢 Count", COUNT_OPTIONS, "count", p, ab, 4)
        button_group("📌 Situation", SITUATION_OPTIONS, "situation", p, ab, 4)

    with right:
        strike_zone_visual(p, ab)

    if contact_fields_should_show(data.get("result", "")):
         button_group("⚾ Contact", CONTACT_TYPE_OPTIONS, "contact_type", p, ab, 5)
         field_direction_visual(p, ab)
         button_group("🔥 Quality", CONTACT_QUALITY_OPTIONS, "quality", p, ab, 3)
    else:
         st.info("Contact, direction and quality are not needed for this result.")

    data["comment"] = st.text_area(
        "Comment",
        value=data.get("comment", ""),
        key=f"comment_{p}_{ab}",
        placeholder="Example: Hard LD to CF off FB middle-middle. Good swing decision.",
    )

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Clear This AB", use_container_width=True):
            st.session_state.chart_data[p][f"ab_{ab}"] = blank_ab()
            autosave()
            st.rerun()

    with c2:
        if st.button("Save & Next AB", use_container_width=True):
            autosave()

            if st.session_state.selected_ab < st.session_state.active_abs:
                st.session_state.selected_ab += 1
            elif st.session_state.active_abs < MAX_ABS:
                st.session_state.active_abs += 1
                st.session_state.selected_ab += 1

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def live_ab_card():
    p = st.session_state.selected_player
    ab = st.session_state.selected_ab
    data = st.session_state.chart_data[p][f"ab_{ab}"]

    player = st.session_state.lineup[p]
    name = player.get("name", "").strip() or f"Player {p + 1}"

    chips = [
        f"Pitch: {data.get('pitch','')} {data.get('velo','')}",
        f"Count: {data.get('count','')}",
        f"Zone: {data.get('zone','')}",
        f"Contact: {data.get('contact_type','')}",
        f"Direction: {data.get('direction','')}",
        f"Quality: {data.get('quality','')}",
        f"Situation: {data.get('situation','')}",
    ]

    chips_html = "".join(
        [f"<span class='chip'>{chip}</span>" for chip in chips]
    )

    comment = data.get("comment", "")

    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Live AB Card</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
<div class="ab-card-filled">
    <div class="ab-number">{p + 1}. {name} • AB {ab}</div>
    <div class="ab-result">{result_dot(data.get("result",""))} {data.get("result") or "-"}</div>
    <div>{chips_html}</div>
    <hr>
    <div class="muted">{comment}</div>
</div>
        """,
        unsafe_allow_html=True,
    )

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
            file_name="tigervision_chart.csv",
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
            file_name="tigervision_scorebook.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
# MAIN
# =========================

init_state()
css()
theme_toggle()

if st.session_state.screen == "game_center":
    game_center()
else:
    header()

    nav1, nav2, nav3 = st.columns([1, 1, 1])

    with nav1:
        if st.button("⬅️ Game Center", use_container_width=True):
            st.session_state.screen = "game_center"
            st.rerun()

    with nav2:
        if st.button("💾 Save Game", use_container_width=True):
            save_current_game()

    with nav3:
        if st.button("➕ New Game", use_container_width=True):
            new_game()

    game_info_panel()
    lineup_panel()

    left, middle, right = st.columns([1.05, 2.25, 1.25])

    with left:
        lineup_quick_panel()
        ab_timeline()

    with middle:
        quick_chart_panel()

    with right:
        live_ab_card()
        exports_panel()