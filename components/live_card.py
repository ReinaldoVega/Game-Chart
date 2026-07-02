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

    chips_html = "".join([
        f"<span class='chip'>Progress: {progress}</span>",
        f"<span class='chip'>Next: {next_step}</span>",
        f"<span class='chip'>Pitch: {data.get('pitch','')} {data.get('velo','')}</span>",
        f"<span class='chip'>Count: {data.get('count','')}</span>",
        f"<span class='chip'>Zone: {data.get('zone','')}</span>",
        f"<span class='chip'>Contact: {data.get('contact_type','')}</span>",
        f"<span class='chip'>Direction: {data.get('direction','')}</span>",
        f"<span class='chip'>Quality: {data.get('quality','')}</span>",
        f"<span class='chip'>Situation: {data.get('situation','')}</span>",
    ])

    panel_start()
    section_title("Live AB Card")

    html = f"""
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
            {comment if comment else "No comment yet."}
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

    if next_step == "Complete":
        st.success("✅ At-bat complete")
    else:
        st.info(f"🧠 Next: {next_step}")

    panel_end()