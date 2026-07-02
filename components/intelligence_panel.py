# components/intelligence_panel.py

import streamlit as st

from components.ui import panel_start, panel_end, section_title
from intelligence import (
    build_team_summary,
    build_player_summaries,
    generate_game_observations,
)


def render_intelligence_panel():
    lineup = st.session_state.lineup
    chart_data = st.session_state.chart_data
    active_abs = st.session_state.active_abs

    summary = build_team_summary(lineup, chart_data, active_abs)
    players = build_player_summaries(lineup, chart_data, active_abs)
    observations = generate_game_observations(summary)

    panel_start()
    section_title("🧠 Intelligence")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Charted ABs", summary["total_abs"])
        st.metric("Hits", summary["hits"])

    with c2:
        st.metric("Hard Contact", summary["hard_contacts"])
        st.metric("Chase Events", summary["chase_events"])

    with c3:
        st.metric("Strikeouts", summary["strikeouts"])
        st.metric("Top Direction", summary["top_direction"])

    st.markdown("#### Game Observations")
    for obs in observations:
        st.write(f"• {obs}")

    st.markdown("#### Player Snapshots")

    for name, s in players.items():
        with st.expander(name, expanded=False):
            st.write(
                f"PA: {s['PA']} | H: {s['H']} | BB/HBP: {s['BB_HBP']} | "
                f"K: {s['K']} | Hard: {s['Hard']} | Chase: {s['Chase']}"
            )
            st.caption(
                f"Best Pitch: {s['Best Pitch']} | Common Zone: {s['Common Zone']} | "
                f"Main Direction: {s['Main Direction']}"
            )

    panel_end()