# components/header.py

import streamlit as st


def render_header():
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


def render_game_center_header():
    st.markdown(
        """
        <div class="main-header">
            <h1>🐅 TigerVision</h1>
            <p>Game Center — create, continue, and manage charted games.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )