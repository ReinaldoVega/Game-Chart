import streamlit as st


def get_theme():

    mode = st.session_state.get("theme_mode", "Dark")

    if mode == "Light":

        return {

            "background": "#F4F7FB",

            "panel": "#FFFFFF",

            "card": "#FFFFFF",

            "card2": "#F8FAFC",

            "text": "#0F172A",

            "muted": "#64748B",

            "border": "#D7DEE8",

            "primary": "#0C2340",

            "accent": "#FA4616",

            "success": "#16A34A",

            "warning": "#EAB308",

            "danger": "#DC2626",

            "shadow": "0 10px 25px rgba(15,23,42,.08)",

            "button":
                "linear-gradient(180deg,#FFFFFF,#F3F4F6)",

            "header":
                "linear-gradient(135deg,#FFFFFF,#F3F4F6)"
        }

    return {

        "background": "#07111F",

        "panel": "#0B1B2E",

        "card": "#102A44",

        "card2": "#0F2237",

        "text": "#F8FAFC",

        "muted": "#94A3B8",

        "border": "#223C58",

        "primary": "#0C2340",

        "accent": "#FA4616",

        "success": "#22C55E",

        "warning": "#FACC15",

        "danger": "#EF4444",

        "shadow": "0 18px 40px rgba(0,0,0,.30)",

        "button":
            "linear-gradient(180deg,#163B63,#0B1B2E)",

        "header":
            "linear-gradient(135deg,#0C2340,#07111F)"
    }


def inject_theme():

    t = get_theme()

    st.markdown(
        f"""
<style>

.stApp{{
    background:{t['background']};
    color:{t['text']};
}}

.main-header{{
    background:{t['header']};
    border-radius:24px;
    padding:24px;
    border-left:8px solid {t['accent']};
    box-shadow:{t['shadow']};
    margin-bottom:18px;
}}

.panel{{
    background:{t['panel']};
    border:1px solid {t['border']};
    border-radius:20px;
    padding:18px;
    margin-bottom:18px;
}}

.section-title{{
    font-size:20px;
    font-weight:900;
    margin-bottom:12px;
}}

.muted{{
    color:{t['muted']};
}}

.chip{{
    display:inline-block;
    padding:6px 10px;
    margin:3px;
    border-radius:999px;
    background:{t['card2']};
    border:1px solid {t['border']};
    font-size:11px;
    font-weight:700;
}}

.ab-card{{
    background:{t['card']};
    border-radius:18px;
    border:1px solid {t['border']};
    padding:14px;
}}

div[data-testid="stButton"] button{{
    background:{t['button']};
    color:{t['text']};
    border-radius:14px;
    border:1px solid {t['border']};
    font-weight:800;
    min-height:44px;
    transition:.15s;
}}

div[data-testid="stButton"] button:hover{{
    border-color:{t['accent']};
    transform:translateY(-2px);
}}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div {{
    border-radius:12px;
}}

</style>
""",
        unsafe_allow_html=True,
    )


def theme_switch():

    c1, c2 = st.columns([1, 1])

    with c1:

        if st.button("🌙 Dark", use_container_width=True):

            st.session_state.theme_mode = "Dark"

            st.rerun()

    with c2:

        if st.button("☀️ Light", use_container_width=True):

            st.session_state.theme_mode = "Light"

            st.rerun()