# components/topbar.py

import streamlit as st


def render_topbar(save_callback, new_game_callback):
    left, center, right = st.columns([1.2, 1.5, 1.3])

    with left:
        st.markdown(
            """
            <div class="tv-kpi">
                <div class="tv-kpi-label">TigerVision</div>
                <div class="tv-kpi-value">🐅 Chart</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with center:
        n1, n2, n3 = st.columns(3)

        with n1:
            if st.button("⬅️ Game Center", use_container_width=True):
                st.session_state.screen = "game_center"
                st.rerun()

        with n2:
            if st.button("💾 Save", use_container_width=True):
                save_callback()

        with n3:
            if st.button("➕ New", use_container_width=True):
                new_game_callback()

    with right:
        mode = st.session_state.get("theme_mode", "Dark")
        st.markdown(
            f"""
            <div class="tv-kpi">
                <div class="tv-kpi-label">Mode</div>
                <div class="tv-kpi-value">{'🌙 Dark' if mode == 'Dark' else '☀️ Light'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )