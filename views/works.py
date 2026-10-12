# -*- coding: utf-8 -*-
"""作品与工具：几件自己做过的小东西。文案在 site_data.WORKS 里改。"""
import streamlit as st

import site_data as sd
import ui

ui.apply_theme()
ui.sidebar()

ui.page_title(sd.PAGES["works"][ui.lang()])

for item in ui.L(sd.WORKS):
    ui.card(item["title"], item.get("detail") or item["summary"], tags=item.get("tags"))

ui.footer()
