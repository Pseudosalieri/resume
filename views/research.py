# -*- coding: utf-8 -*-
"""科研与项目：两段科研经历，内容逐字来自 Word 简历。"""
import streamlit as st

import site_data as sd
import ui

ui.apply_theme()
ui.sidebar()

labels = ui.L(sd.LABELS)
heading = sd.PAGES["research"][ui.lang()]
st.title(heading)

for i, item in enumerate(ui.rdata().RESEARCH):
    ui.heading(item["title"])
    st.caption(f"{item['period']}　|　{item['role']}")
    st.markdown(item["detail"])
    if i != len(ui.rdata().RESEARCH) - 1:
        st.divider()

ui.footer()
