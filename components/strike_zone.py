# components/strike_zone.py

import streamlit as st
from components.canvas_engine import interactive_strike_zone


def render_strike_zone(p, ab, autosave_func):
    key = f"ab_{ab}"
    current = st.session_state.chart_data[p][key].get("zone", "")

    st.markdown("### 🎯 Strike Zone")
    st.caption(f"Selected: {current or 'None'}")

    selected_zone = interactive_strike_zone(
        selected_zone=current,
        key=f"interactive_zone_{p}_{ab}",
    )

    if selected_zone:
        st.session_state.chart_data[p][key]["zone"] = selected_zone
        autosave_func()
        st.rerun()

    if st.button("Clear Zone", key=f"clear_zone_{p}_{ab}", use_container_width=True):
        st.session_state.chart_data[p][key]["zone"] = ""
        autosave_func()
        st.rerun()