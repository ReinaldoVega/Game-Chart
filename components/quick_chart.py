# components/quick_chart.py

import streamlit as st

from components.ui import (
    button_group,
    result_dot,
    panel_start,
    panel_end,
    section_title,
)
from rules_engine import contact_fields_should_show
from workflow_engine import get_next_step_label, get_progress_text
from components.strike_zone import render_strike_zone
from components.field import render_field_direction
from components.coach_assistant import render_coach_assistant

# =========================
# LINEUP QUICK PANEL
# =========================

def render_lineup_quick_panel():
    panel_start()
    section_title("Lineup")

    for i, player in enumerate(st.session_state.lineup):
        name = player.get("name", "").strip() or f"Player {i + 1}"
        pos = player.get("position", "")
        bats = player.get("bats", "")

        dots = ""
        for ab in range(1, st.session_state.active_abs + 1):
            r = st.session_state.chart_data[i][f"ab_{ab}"].get("result", "")
            dots += result_dot(r)

        label = f"{i + 1}. {name}"
        if pos:
            label += f" | {pos}"
        if bats:
            label += f" | {bats}"

        if st.button(label, key=f"pick_player_{i}", use_container_width=True):
            st.session_state.selected_player = i
            st.rerun()

        st.markdown(
            f"<div class='muted' style='margin-bottom:8px;'>{dots}</div>",
            unsafe_allow_html=True,
        )

        for sub in player.get("subs", []):
            if sub.get("name"):
                st.markdown(
                    f"<div class='muted'>↳ {sub.get('role')} {sub.get('name')} "
                    f"{sub.get('position','')} Inn {sub.get('inning','')}</div>",
                    unsafe_allow_html=True,
                )

    panel_end()


# =========================
# AB TIMELINE
# =========================

def render_ab_timeline(autosave_func):
    panel_start()
    section_title("At-Bats")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("+ Add AB", use_container_width=True):
            if st.session_state.active_abs < st.session_state.MAX_ABS_VALUE:
                st.session_state.active_abs += 1
                autosave_func()
                st.rerun()

    with c2:
        if st.button("- Remove AB", use_container_width=True):
            if st.session_state.active_abs > st.session_state.DEFAULT_ABS_VALUE:
                st.session_state.active_abs -= 1

                if st.session_state.selected_ab > st.session_state.active_abs:
                    st.session_state.selected_ab = st.session_state.active_abs

                autosave_func()
                st.rerun()

    p = st.session_state.selected_player

    for ab in range(1, st.session_state.active_abs + 1):
        data = st.session_state.chart_data[p][f"ab_{ab}"]

        label = f"AB {ab} {result_dot(data.get('result', ''))}"
        if data.get("result"):
            label += f" {data.get('result')}"

        if st.button(label, key=f"pick_ab_{ab}", use_container_width=True):
            st.session_state.selected_ab = ab
            st.rerun()

    panel_end()


# =========================
# STRIKE ZONE
# =========================

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


# =========================
# FIELD DIRECTION
# =========================

def render_field_direction(p, ab, autosave_func):
    st.markdown("### 🧤 Field Direction")

    row1 = st.columns(3)
    with row1[0]:
        button_group("", ["LF"], "direction", p, ab, autosave_func, 1)
    with row1[1]:
        button_group("", ["CF"], "direction", p, ab, autosave_func, 1)
    with row1[2]:
        button_group("", ["RF"], "direction", p, ab, autosave_func, 1)

    row2 = st.columns(4)
    with row2[0]:
        button_group("", ["3B"], "direction", p, ab, autosave_func, 1)
    with row2[1]:
        button_group("", ["SS"], "direction", p, ab, autosave_func, 1)
    with row2[2]:
        button_group("", ["2B"], "direction", p, ab, autosave_func, 1)
    with row2[3]:
        button_group("", ["1B"], "direction", p, ab, autosave_func, 1)

    row3 = st.columns(2)
    with row3[0]:
        button_group("", ["P"], "direction", p, ab, autosave_func, 1)
    with row3[1]:
        button_group("", ["C"], "direction", p, ab, autosave_func, 1)


# =========================
# QUICK CHART PANEL
# =========================

def render_quick_chart_panel(
    result_options,
    pitch_options,
    count_options,
    situation_options,
    contact_type_options,
    contact_quality_options,
    autosave_func,
):
    p = st.session_state.selected_player
    ab = st.session_state.selected_ab

    data = st.session_state.chart_data[p][f"ab_{ab}"]
    player = st.session_state.lineup[p]

    name = player.get("name", "").strip() or f"Player {p + 1}"
    subs = [s for s in player.get("subs", []) if s.get("name")]

    panel_start()
    section_title(f"Quick Chart — {p + 1}. {name} | AB {ab}")

    render_coach_assistant(data)

    batter_options = ["Starter"] + [
        f"{s.get('role')} - {s.get('name')}" for s in subs
    ]

    data["batter"] = st.selectbox(
        "Who took this AB?",
        batter_options,
        index=batter_options.index(data.get("batter", "Starter"))
        if data.get("batter", "Starter") in batter_options
        else 0,
        key=f"batter_{p}_{ab}",
    )

    left, right = st.columns([1.1, 1])

    with left:
        button_group("🟢 Result", result_options, "result", p, ab, autosave_func, 4)
        button_group("🟣 Pitch", pitch_options, "pitch", p, ab, autosave_func, 4)

        data["velo"] = st.text_input(
            "Pitch Velo",
            value=data.get("velo", ""),
            key=f"velo_{p}_{ab}",
            placeholder="94.5",
        )

        button_group("🔢 Count", count_options, "count", p, ab, autosave_func, 4)
        button_group("📌 Situation", situation_options, "situation", p, ab, autosave_func, 4)

    with right:
        render_strike_zone(p, ab, autosave_func)

        if contact_fields_should_show(data.get("result", "")):
            button_group(
                "⚾ Contact",
                contact_type_options,
                "contact_type",
                p,
                ab,
                autosave_func,
                5,
            )
            render_field_direction(p, ab, autosave_func)
            button_group(
                "🔥 Quality",
                contact_quality_options,
                "quality",
                p,
                ab,
                autosave_func,
                3,
            )
        else:
            st.info("Contact, direction and quality are not needed for this result.")

    data["comment"] = st.text_area(
        "Comment",
        value=data.get("comment", ""),
        key=f"comment_{p}_{ab}",
        placeholder="Example: Hard LD to CF off FB middle-middle. Good swing decision.",
    )

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Clear This AB", use_container_width=True):
            st.session_state.chart_data[p][f"ab_{ab}"] = {
                "batter": "Starter",
                "result": "",
                "pitch": "",
                "velo": "",
                "count": "",
                "zone": "",
                "contact_type": "",
                "direction": "",
                "quality": "",
                "situation": "",
                "comment": "",
            }
            autosave_func()
            st.rerun()

    with c2:
        if st.button("Save & Next AB", use_container_width=True):
            autosave_func()

            if st.session_state.selected_ab < st.session_state.active_abs:
                st.session_state.selected_ab += 1
            elif st.session_state.active_abs < st.session_state.MAX_ABS_VALUE:
                st.session_state.active_abs += 1
                st.session_state.selected_ab += 1

            st.rerun()

    panel_end()