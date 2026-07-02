# components/strike_zone.py

import streamlit as st


def zone_btn(label, value, p, ab, autosave_func, css_class="zone-cell"):
    key = f"ab_{ab}"
    current = st.session_state.chart_data[p][key].get("zone", "")
    selected = current == value

    button_label = f"✅ {label}" if selected else label

    if st.button(
        button_label,
        key=f"zone_svg_{p}_{ab}_{value}",
        use_container_width=True,
    ):
        st.session_state.chart_data[p][key]["zone"] = value
        autosave_func()
        st.rerun()


def render_strike_zone(p, ab, autosave_func):
    current = st.session_state.chart_data[p][f"ab_{ab}"].get("zone", "")

    st.markdown("### 🎯 Strike Zone")
    st.caption(f"Selected: {current or 'None'}")

    st.markdown(
        """
        <div style="
            text-align:center;
            font-weight:900;
            color:var(--tv-muted);
            margin-bottom:4px;">
            CHASE UP
        </div>
        """,
        unsafe_allow_html=True,
    )

    top = st.columns([1, 2, 1])
    with top[1]:
        zone_btn("⬆️ UP", "Chase Up", p, ab, autosave_func)

    st.markdown(
        """
        <div style="
            border:2px solid var(--tv-accent);
            border-radius:18px;
            padding:10px;
            background:linear-gradient(180deg,var(--tv-surface2),var(--tv-surface));
            box-shadow:var(--tv-soft-shadow);
            margin:8px 0;">
        """,
        unsafe_allow_html=True,
    )

    rows = [
        [("1", "1"), ("2", "2"), ("3", "3")],
        [("4", "4"), ("5", "5"), ("6", "6")],
        [("7", "7"), ("8", "8"), ("9", "9")],
    ]

    for row in rows:
        cols = st.columns(3)
        for col, (label, value) in zip(cols, row):
            with col:
                zone_btn(label, value, p, ab, autosave_func)

    st.markdown("</div>", unsafe_allow_html=True)

    side1, side2 = st.columns(2)

    with side1:
        zone_btn("⬅️ IN", "Chase In", p, ab, autosave_func)

    with side2:
        zone_btn("AWAY ➡️", "Chase Away", p, ab, autosave_func)

    bottom = st.columns([1, 2, 1])
    with bottom[1]:
        zone_btn("⬇️ DOWN", "Chase Down", p, ab, autosave_func)

    if st.button("Clear Zone", key=f"clear_zone_{p}_{ab}", use_container_width=True):
        st.session_state.chart_data[p][f"ab_{ab}"]["zone"] = ""
        autosave_func()
        st.rerun()