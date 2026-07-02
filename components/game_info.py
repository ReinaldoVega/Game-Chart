# components/game_info.py

import streamlit as st
from datetime import date


def render_game_info_panel():
    with st.expander("Game Info", expanded=False):
        c1, c2, c3, c4, c5, c6, c7 = st.columns(
            [1, 1.1, 1.3, 0.8, 0.8, 0.8, 0.8]
        )

        with c1:
            d = st.date_input(
                "Date",
                value=date.fromisoformat(st.session_state.game_info["date"]),
            )
            st.session_state.game_info["date"] = str(d)

        with c2:
            st.session_state.game_info["team"] = st.text_input(
                "Team",
                st.session_state.game_info["team"],
            )

        with c3:
            st.session_state.game_info["opponent"] = st.text_input(
                "Opponent",
                st.session_state.game_info["opponent"],
            )

        with c4:
            opts = ["", "Home", "Away"]
            st.session_state.game_info["home_away"] = st.selectbox(
                "H/A",
                opts,
                index=opts.index(st.session_state.game_info.get("home_away", "")),
            )

        with c5:
            st.session_state.game_info["game_number"] = st.text_input(
                "Game #",
                st.session_state.game_info["game_number"],
            )

        with c6:
            st.session_state.game_info["inning"] = st.text_input(
                "Inning",
                st.session_state.game_info.get("inning", ""),
            )

        with c7:
            st.session_state.game_info["score"] = st.text_input(
                "Score",
                st.session_state.game_info.get("score", ""),
            )

        st.session_state.game_info["notes"] = st.text_area(
            "General Notes",
            st.session_state.game_info["notes"],
        )