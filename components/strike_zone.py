# components/strike_zone.py

import streamlit as st


def strike_zone_button(label, value, p, ab, autosave_func):
    key = f"ab_{ab}"
    current = st.session_state.chart_data[p][key].get("zone", "")

    selected = current == value
    display = f"🟧 {label}" if selected else label

    if st.button(
        display,
        key=f"strike_zone_{p}_{ab}_{value}",
        use_container_width=True,
    ):
        st.session_state.chart_data[p][key]["zone"] = value
        autosave_func()
        st.rerun()


def render_strike_zone(p, ab, autosave_func):
    st.markdown("### 🎯 Strike Zone")
    st.caption("Tap pitch location")

    chase_up = st.columns([1, 2, 1])
    with chase_up[1]:
        strike_zone_button("⬆️ Chase Up", "Chase Up", p, ab, autosave_func)

    zone_rows = [
        [("1", "1"), ("2", "2"), ("3", "3")],
        [("4", "4"), ("5", "5"), ("6", "6")],
        [("7", "7"), ("8", "8"), ("9", "9")],
    ]

    for row in zone_rows:
        cols = st.columns(3)
        for col, (label, value) in zip(cols, row):
            with col:
                strike_zone_button(label, value, p, ab, autosave_func)

    chase_sides = st.columns(2)

    with chase_sides[0]:
        strike_zone_button("⬅️ Chase In", "Chase In", p, ab, autosave_func)

    with chase_sides[1]:
        strike_zone_button("➡️ Chase Away", "Chase Away", p, ab, autosave_func)

    chase_down = st.columns([1, 2, 1])
    with chase_down[1]:
        strike_zone_button("⬇️ Chase Down", "Chase Down", p, ab, autosave_func)

    if st.button("Clear Zone", key=f"clear_zone_{p}_{ab}", use_container_width=True):
        st.session_state.chart_data[p][f"ab_{ab}"]["zone"] = ""
        autosave_func()
        st.rerun()