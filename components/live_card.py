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

    chips = [
        f"Progress: {progress}",
        f"Next: {next_step}",
        f"Pitch: {data.get('pitch','')} {data.get('velo','')}",
        f"Count: {data.get('count','')}",
        f"Zone: {data.get('zone','')}",
        f"Contact: {data.get('contact_type','')}",
        f"Direction: {data.get('direction','')}",
        f"Quality: {data.get('quality','')}",
        f"Situation: {data.get('situation','')}",
    ]

    chips_html = "".join(
        [f"<span class='chip'>{chip}</span>" for chip in chips if chip.strip()]
    )

    result = data.get("result", "")
    comment = data.get("comment", "")

    panel_start()
    section_title("Live AB Card")

    st.markdown(
        f"""
        <div class="ab-card">
            <div class="muted" style="font-weight:900;">
                {p + 1}. {name} • AB {ab}
            </div>

            <div style="font-size:34px;font-weight:1000;margin:8px 0;">
                {result_dot(result)} {result or "-"}
            </div>

            <div>
                {chips_html}
            </div>

            <hr>

            <div class="muted">
                {comment or "No comment yet."}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if next_step == "Complete":
        st.success("✅ At-bat complete")
    else:
        st.info(f"🧠 Next: {next_step}")

    panel_end()