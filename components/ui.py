# components/ui.py

import streamlit as st
from rules_engine import apply_result_rules


def result_dot(result):
    if result in ["1B", "2B", "3B"]:
        return "🟢"
    if result == "HR":
        return "🟠"
    if result in ["BB", "HBP"]:
        return "🔵"
    if "K" in str(result):
        return "🔴"
    if result:
        return "⚫"
    return "⚪"


def styled_label(field, opt, selected=False):
    prefix = ""

    if field == "result":
        if opt in ["1B", "2B", "3B"]:
            prefix = "🟢"
        elif opt == "HR":
            prefix = "🟠"
        elif opt in ["BB", "HBP"]:
            prefix = "🔵"
        elif "K" in opt:
            prefix = "🔴"
        else:
            prefix = "⚫"
    elif field == "pitch":
        prefix = "🟣"
    elif field == "zone":
        prefix = "🟧"
    elif field == "quality":
        prefix = "🟢" if opt in ["Barrel", "Hard Hit"] else "🟡" if opt == "Solid" else "🔴"
    elif field == "direction":
        prefix = "➡️"
    elif field == "contact_type":
        prefix = "⚾"
    elif field == "count":
        prefix = "🔢"
    elif field == "situation":
        prefix = "📌"

    label = f"{prefix} {opt}".strip()
    return f"✅ {label}" if selected else label


def button_group(title, options, field, p, ab, autosave_func=None, cols_count=4):
    if title:
        st.markdown(f"**{title}**")

    key = f"ab_{ab}"
    current = st.session_state.chart_data[p][key].get(field, "")

    for start in range(0, len(options), cols_count):
        row = options[start:start + cols_count]
        cols = st.columns(len(row))

        for col, opt in zip(cols, row):
            selected = current == opt
            label = styled_label(field, opt, selected)

            with col:
                if st.button(
                    label,
                    key=f"{field}_{p}_{ab}_{opt}",
                    use_container_width=True,
                ):
                    st.session_state.chart_data[p][key][field] = opt

                    if field == "result":
                        st.session_state.chart_data[p][key], note = apply_result_rules(
                            st.session_state.chart_data[p][key]
                        )
                        if note:
                            st.toast(note)

                    if autosave_func:
                        autosave_func()

                    st.rerun()


def panel_start():
    st.markdown("<div class='panel'>", unsafe_allow_html=True)


def panel_end():
    st.markdown("</div>", unsafe_allow_html=True)


def section_title(text):
    st.markdown(f"<div class='section-title'>{text}</div>", unsafe_allow_html=True)


def chip(text):
    st.markdown(f"<span class='chip'>{text}</span>", unsafe_allow_html=True)


def chips(items):
    html = "".join([f"<span class='chip'>{item}</span>" for item in items])
    st.markdown(html, unsafe_allow_html=True)