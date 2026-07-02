# components/coach_assistant.py

import streamlit as st
from workflow_engine import get_next_step_label, get_progress_text


def get_tip(next_step, data):
    result = data.get("result", "")

    if next_step == "Result":
        return "Start by selecting the official result of the at-bat."

    if next_step == "Pitch Type":
        return "Select the pitch that finished the at-bat."

    if next_step == "Pitch Location":
        return "Tap the final pitch location in the strike zone."

    if next_step == "Field Direction":
        if result in ["1B", "2B", "3B", "HR"]:
            return "Select where the ball was hit."
        return "Select the defender or area involved in the out."

    if next_step == "Contact Type":
        return "Separate ball flight from quality. Example: LD can be soft, solid, hard, or barrel."

    if next_step == "Contact Quality":
        return "Grade the quality of contact, not just the result."

    if next_step == "Count":
        return "Record the count when the at-bat ended."

    if next_step == "Complete":
        return "This at-bat has all required fields."

    return "Continue completing the next important detail."


def render_progress_bar(progress):
    try:
        completed, total = progress.split("/")
        completed = int(completed)
        total = int(total)
        pct = completed / total if total else 0
    except Exception:
        pct = 0

    st.progress(pct)


def render_coach_assistant(data):
    next_step = get_next_step_label(data)
    progress = get_progress_text(data)
    tip = get_tip(next_step, data)

    st.markdown("### 🧠 Coach Assistant")

    render_progress_bar(progress)

    if next_step == "Complete":
        st.success("✅ At-bat complete")
    else:
        st.info(f"Next: {next_step}")

    st.caption(tip)