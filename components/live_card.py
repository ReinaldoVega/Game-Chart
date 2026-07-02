# components/live_card.py

import streamlit as st

from components.ui import result_dot, panel_start, panel_end, section_title
from workflow_engine import get_next_step_label, get_progress_text


def render_live_ab_card():
    p = st.session_state.selected_player
    ab = st.session_state.selected_ab

    data = st.session_state.chart_data[p][f"ab_{ab}"]
    player = st.session_state.lineup[p]

    name = player.get("name", "").strip() or f"Player {p + 1}"

    next_step = get_next_step_label(data)
    progress = get_progress_text(data)

    result = data.get("result", "")
    comment = data.get("comment", "")

    panel_start()
    section_title("Live AB Card")

    st.caption(f"{p + 1}. {name} • AB {ab}")

    st.markdown(f"## {result_dot(result)} {result or '-'}")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Progress", progress)
        st.metric("Pitch", f"{data.get('pitch','')} {data.get('velo','')}".strip() or "-")
        st.metric("Zone", data.get("zone", "") or "-")
        st.metric("Contact", data.get("contact_type", "") or "-")

    with c2:
        st.metric("Next", next_step)
        st.metric("Count", data.get("count", "") or "-")
        st.metric("Direction", data.get("direction", "") or "-")
        st.metric("Quality", data.get("quality", "") or "-")

    st.divider()

    st.caption("Comment")
    st.write(comment or "No comment yet.")

    if next_step == "Complete":
        st.success("✅ At-bat complete")
    else:
        st.info(f"🧠 Next: {next_step}")

    panel_end()