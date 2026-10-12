# -*- coding: utf-8 -*-
"""科研与项目：两段科研经历，内容逐字来自 Word 简历。"""
import streamlit as st

import site_data as sd
import ui

ui.apply_theme()
ui.sidebar()

ui.page_title(sd.PAGES["research"][ui.lang()])

for item in ui.rdata().RESEARCH:
    ui.card(item["title"], item["detail"],
            meta=f"{item['period']}　·　{item['role']}",
            tags=[item["role"]])

ui.footer()
