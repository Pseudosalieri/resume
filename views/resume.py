# -*- coding: utf-8 -*-
"""简历：只提供最新版 PDF 的下载。"""
import streamlit as st

import site_data as sd
import ui

ui.apply_theme()
ui.sidebar()

labels = ui.L(sd.LABELS)
st.title(sd.PAGES["resume"][ui.lang()])
st.markdown(labels["download_hint"])

pdf = ui.asset(ui.rdata().PROFILE["resume_pdf"])
if pdf:
    st.download_button(f"⬇️  {labels['download']}", pdf.read_bytes(),
                       file_name=pdf.name, mime="application/pdf")
else:
    st.info("未找到简历 PDF")

st.caption(labels["papers_note"])

ui.footer()
