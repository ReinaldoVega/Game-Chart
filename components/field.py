# components/field.py

import streamlit as st
from components.ui import button_group


def render_field_direction(p, ab, autosave_func):
    st.markdown("### 🧤 Field Direction")

    row1 = st.columns([1, 1, 1])
    with row1[0]:
        button_group("", ["LF"], "direction", p, ab, autosave_func, 1)
    with row1[1]:
        button_group("", ["CF"], "direction", p, ab, autosave_func, 1)
    with row1[2]:
        button_group("", ["RF"], "direction", p, ab, autosave_func, 1)

    row2 = st.columns([1, 1, 1, 1])
    with row2[0]:
        button_group("", ["3B"], "direction", p, ab, autosave_func, 1)
    with row2[1]:
        button_group("", ["SS"], "direction", p, ab, autosave_func, 1)
    with row2[2]:
        button_group("", ["2B"], "direction", p, ab, autosave_func, 1)
    with row2[3]:
        button_group("", ["1B"], "direction", p, ab, autosave_func, 1)

    row3 = st.columns([1, 1])
    with row3[0]:
        button_group("", ["P"], "direction", p, ab, autosave_func, 1)
    with row3[1]:
        button_group("", ["C"], "direction", p, ab, autosave_func, 1)