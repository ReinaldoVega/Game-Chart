# components/coach_assistant.py

import streamlit as st
from workflow_engine import get_next_step_label, get_progress_text


def render_coach_assistant(data):
    next_step = get_next_step_label(data)
    progress = get_progress_text(data)

    st.markdown("### 🧠 Coach Assistant")

    if next_step == "Complete":
        st.success(f"✅ At-bat complete | Progress {progress}")
    else:
        st.info(f"Next: {next_step} | Progress {progress}")