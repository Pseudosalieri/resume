# -*- coding: utf-8 -*-
"""首页：一段自我介绍 + 方向 + 近况。"""
import streamlit as st

import site_data as sd
import ui

ui.apply_theme()
ui.sidebar()

profile = ui.rdata().PROFILE
site = ui.L(sd.SITE)
labels = ui.L(sd.LABELS)

ui.hero(site["name"], site["intro"], photo=ui.asset(profile["avatar"]))

# 联系方式：简历下载只放在「简历」页，这里不重复放入口
fields = dict(profile["fields"])
email = fields.get(ui.L({"zh": "邮箱", "en": "Email"}))
col1, col2 = st.columns(2)
with col1:
    if email:
        st.link_button(f"✉️  {labels['send_email']}", f"mailto:{email}",
                       use_container_width=True)
with col2:
    if sd.LINKS.get("github"):
        st.link_button("💻  GitHub", sd.LINKS["github"], use_container_width=True)

ui.section(ui.L({"zh": "关于我", "en": "About me"}))
ui.card("", site["bio"])

ui.section(site["keywords_title"])
ui.chips(site["keywords"])

ui.section(site["now_title"])
ui.bullet_list(site["now"])

ui.footer()
