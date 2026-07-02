# components/field.py

import streamlit as st
from components.ui import button_group


def field_btn(label, value, p, ab, autosave_func):
    key = f"ab_{ab}"
    current = st.session_state.chart_data[p][key].get("direction", "")
    selected = current == value

    display = f"✅ {label}" if selected else label

    if st.button(
        display,
        key=f"field_{p}_{ab}_{value}",
        use_container_width=True,
    ):
        st.session_state.chart_data[p][key]["direction"] = value
        autosave_func()
        st.rerun()


def render_field_direction(p, ab, autosave_func):
    current = st.session_state.chart_data[p][f"ab_{ab}"].get("direction", "")

    st.markdown("### 🏟️ Field Direction")
    st.caption(f"Selected: {current or 'None'}")

    st.markdown(
        """
        <div style="
            border:2px solid var(--tv-border);
            border-radius:24px;
            padding:16px;
            background:
                radial-gradient(circle at center bottom, rgba(250,70,22,.16), transparent 34%),
                linear-gradient(180deg,var(--tv-surface2),var(--tv-surface));
            box-shadow:var(--tv-soft-shadow);
            margin:8px 0 10px 0;">
        """,
        unsafe_allow_html=True,
    )

    # Outfield
    row1 = st.columns([1, 1, 1])
    with row1[0]:
        field_btn("LF", "LF", p, ab, autosave_func)
    with row1[1]:
        field_btn("CF", "CF", p, ab, autosave_func)
    with row1[2]:
        field_btn("RF", "RF", p, ab, autosave_func)

    # Infield middle
    row2 = st.columns([0.6, 1, 1, 0.6])
    with row2[1]:
        field_btn("SS", "SS", p, ab, autosave_func)
    with row2[2]:
        field_btn("2B", "2B", p, ab, autosave_func)

    # Corners
    row3 = st.columns([1, 1, 1])
    with row3[0]:
        field_btn("3B", "3B", p, ab, autosave_func)
    with row3[1]:
        field_btn("P", "P", p, ab, autosave_func)
    with row3[2]:
        field_btn("1B", "1B", p, ab, autosave_func)

    # Catcher
    row4 = st.columns([1, 1, 1])
    with row4[1]:
        field_btn("C", "C", p, ab, autosave_func)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Clear Direction", key=f"clear_direction_{p}_{ab}", use_container_width=True):
        st.session_state.chart_data[p][f"ab_{ab}"]["direction"] = ""
        autosave_func()
        st.rerun()