# app.py

import streamlit as st
from datetime import date

from config import *
from database import save_game, get_game

from styles.theme import inject_theme, theme_switch

from components.game_center import render_game_center
from components.header import render_header
from components.game_info import render_game_info_panel
from components.lineup import render_lineup_panel
from components.quick_chart import (
    render_lineup_quick_panel,
    render_ab_timeline,
    render_quick_chart_panel,
)
from components.live_card import render_live_ab_card
from components.exports_panel import render_exports_panel


st.set_page_config(
    page_title="TigerVision",
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


def init_state():
    st.session_state.setdefault("screen", "game_center")
    st.session_state.setdefault("theme_mode", "Dark")
    st.session_state.setdefault("active_abs", DEFAULT_ABS)
    st.session_state.setdefault("selected_player", 0)
    st.session_state.setdefault("selected_ab", 1)

    st.session_state.MAX_ABS_VALUE = MAX_ABS
    st.session_state.DEFAULT_ABS_VALUE = DEFAULT_ABS

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
    st.session_state.screen = "chart"

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

    st.session_state.lineup = [
        {"name": "", "position": "", "bats": "", "subs": []}
        for _ in range(MAX_PLAYERS)
    ]

    st.session_state.chart_data = {}

    for p in range(MAX_PLAYERS):
        st.session_state.chart_data[p] = {}
        for ab in range(1, MAX_ABS + 1):
            st.session_state.chart_data[p][f"ab_{ab}"] = blank_ab()

    st.session_state.active_abs = DEFAULT_ABS
    st.session_state.selected_player = 0
    st.session_state.selected_ab = 1

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


def render_top_nav():
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


def render_chart_screen():
    render_header()
    render_top_nav()

    render_game_info_panel()

    render_lineup_panel(
        POSITION_OPTIONS,
        BATS_OPTIONS,
        PLAYER_ROLE_OPTIONS,
    )

    left, middle, right = st.columns([1.05, 2.25, 1.25])

    with left:
        render_lineup_quick_panel()
        render_ab_timeline(autosave)

    with middle:
        render_quick_chart_panel(
            RESULT_OPTIONS,
            PITCH_OPTIONS,
            COUNT_OPTIONS,
            SITUATION_OPTIONS,
            CONTACT_TYPE_OPTIONS,
            CONTACT_QUALITY_OPTIONS,
            autosave,
        )

    with right:
        render_live_ab_card()
        render_exports_panel()


init_state()
inject_theme()
theme_switch()

if st.session_state.screen == "game_center":
    render_game_center(new_game, open_game)
else:
    render_chart_screen()