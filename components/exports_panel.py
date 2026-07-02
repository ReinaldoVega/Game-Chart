# components/exports_panel.py

import streamlit as st

from components.ui import panel_start, panel_end, section_title
from csv_export import export_chart_csv
from pdf_export import export_chart_pdf


def render_exports_panel():
    panel_start()
    section_title("Export")

    c1, c2 = st.columns(2)

    with c1:
        st.download_button(
            "Download CSV",
            data=export_chart_csv(
                st.session_state.game_info,
                st.session_state.lineup,
                st.session_state.chart_data,
            ),
            file_name="tigervision_chart.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with c2:
        st.download_button(
            "Download PDF",
            data=export_chart_pdf(
                st.session_state.game_info,
                st.session_state.lineup,
                st.session_state.chart_data,
            ),
            file_name="tigervision_scorebook.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    panel_end()