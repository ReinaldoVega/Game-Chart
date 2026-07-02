# styles/theme.py

import streamlit as st


def get_theme():
    mode = st.session_state.get("theme_mode", "Dark")

    if mode == "Light":
        return {
            "name": "Light",
            "background": "#F4F7FB",
            "background_2": "#EAF0F7",
            "surface": "#FFFFFF",
            "surface_2": "#F8FAFC",
            "surface_3": "#EEF2F7",
            "text": "#0F172A",
            "muted": "#64748B",
            "border": "#D7DEE8",
            "primary": "#0C2340",
            "accent": "#FA4616",
            "success": "#16A34A",
            "warning": "#EAB308",
            "danger": "#DC2626",
            "blue": "#2563EB",
            "purple": "#7C3AED",
            "shadow": "0 14px 35px rgba(15,23,42,.10)",
            "soft_shadow": "0 8px 20px rgba(15,23,42,.07)",
            "button": "linear-gradient(180deg,#FFFFFF,#F1F5F9)",
            "header": "linear-gradient(135deg,#FFFFFF,#F1F5F9)",
        }

    return {
        "name": "Dark",
        "background": "#07111F",
        "background_2": "#0A1728",
        "surface": "#0B1B2E",
        "surface_2": "#102A44",
        "surface_3": "#132F4F",
        "text": "#F8FAFC",
        "muted": "#94A3B8",
        "border": "#223C58",
        "primary": "#0C2340",
        "accent": "#FA4616",
        "success": "#22C55E",
        "warning": "#FACC15",
        "danger": "#EF4444",
        "blue": "#60A5FA",
        "purple": "#A78BFA",
        "shadow": "0 20px 45px rgba(0,0,0,.34)",
        "soft_shadow": "0 10px 26px rgba(0,0,0,.22)",
        "button": "linear-gradient(180deg,#163B63,#0B1B2E)",
        "header": "linear-gradient(135deg,#0C2340,#07111F)",
    }


def inject_theme():
    t = get_theme()

    st.markdown(
        f"""
<style>
:root {{
    --tv-bg: {t['background']};
    --tv-bg2: {t['background_2']};
    --tv-surface: {t['surface']};
    --tv-surface2: {t['surface_2']};
    --tv-surface3: {t['surface_3']};
    --tv-text: {t['text']};
    --tv-muted: {t['muted']};
    --tv-border: {t['border']};
    --tv-primary: {t['primary']};
    --tv-accent: {t['accent']};
    --tv-success: {t['success']};
    --tv-warning: {t['warning']};
    --tv-danger: {t['danger']};
    --tv-blue: {t['blue']};
    --tv-purple: {t['purple']};
    --tv-shadow: {t['shadow']};
    --tv-soft-shadow: {t['soft_shadow']};
}}

.stApp {{
    background:
        radial-gradient(circle at top left, rgba(250,70,22,.16), transparent 25%),
        radial-gradient(circle at top right, rgba(12,35,64,.42), transparent 30%),
        linear-gradient(180deg, var(--tv-bg), var(--tv-bg2));
    color: var(--tv-text);
}}

.block-container {{
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}}

.main-header {{
    background: {t['header']};
    border-radius: 28px;
    padding: 24px 28px;
    border: 1px solid var(--tv-border);
    border-left: 9px solid var(--tv-accent);
    box-shadow: var(--tv-shadow);
    margin-bottom: 18px;
}}

.panel {{
    background: rgba(11,27,46,.92);
    background: var(--tv-surface);
    border: 1px solid var(--tv-border);
    border-radius: 24px;
    padding: 18px;
    margin-bottom: 18px;
    box-shadow: var(--tv-soft-shadow);
}}

.section-title {{
    color: var(--tv-text);
    font-size: 20px;
    font-weight: 950;
    letter-spacing: .2px;
    margin-bottom: 12px;
}}

.muted {{
    color: var(--tv-muted);
    font-size: 12px;
}}

.chip {{
    display: inline-block;
    padding: 6px 10px;
    margin: 3px;
    border-radius: 999px;
    background: var(--tv-surface2);
    border: 1px solid var(--tv-border);
    color: var(--tv-text);
    font-size: 11px;
    font-weight: 800;
}}

.ab-card {{
    background: linear-gradient(180deg, var(--tv-surface2), var(--tv-surface));
    border-radius: 22px;
    border: 1px solid var(--tv-border);
    padding: 16px;
    box-shadow: var(--tv-soft-shadow);
}}

.tv-kpi {{
    background: linear-gradient(180deg, var(--tv-surface2), var(--tv-surface));
    border: 1px solid var(--tv-border);
    border-radius: 20px;
    padding: 14px;
    box-shadow: var(--tv-soft-shadow);
}}

.tv-kpi-label {{
    color: var(--tv-muted);
    font-size: 11px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: .8px;
}}

.tv-kpi-value {{
    color: var(--tv-text);
    font-size: 26px;
    font-weight: 1000;
    line-height: 1.1;
}}

div[data-testid="stButton"] button {{
    background: {t['button']};
    color: var(--tv-text);
    border-radius: 16px;
    border: 1px solid var(--tv-border);
    font-weight: 900;
    min-height: 46px;
    transition: .15s ease-in-out;
    box-shadow: 0 2px 0 rgba(0,0,0,.08);
}}

div[data-testid="stButton"] button:hover {{
    border-color: var(--tv-accent);
    transform: translateY(-1px);
    box-shadow: 0 10px 22px rgba(250,70,22,.18);
}}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {{
    background: var(--tv-surface2);
    color: var(--tv-text);
    border: 1px solid var(--tv-border);
    border-radius: 14px;
}}

div[data-testid="stSelectbox"] > div {{
    border-radius: 14px;
}}

.stExpander {{
    border: 1px solid var(--tv-border) !important;
    border-radius: 18px !important;
    overflow: hidden;
    background: var(--tv-surface);
}}

hr {{
    border-color: var(--tv-border);
}}

</style>
""",
        unsafe_allow_html=True,
    )


def theme_switch():
    c1, c2, c3 = st.columns([6, 1, 1])

    with c2:
        if st.button("🌙 Dark", use_container_width=True):
            st.session_state.theme_mode = "Dark"
            st.rerun()

    with c3:
        if st.button("☀️ Light", use_container_width=True):
            st.session_state.theme_mode = "Light"
            st.rerun()