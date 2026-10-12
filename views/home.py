# -*- coding: utf-8 -*-
"""首页：一段自我介绍 + 方向 + 近况 + 入口。"""
import streamlit as st

import site_data as sd
import ui

ui.apply_theme()
ui.sidebar()

profile = ui.rdata().PROFILE
site = ui.L(sd.SITE)
labels = ui.L(sd.LABELS)

ui.hero(site["name"], site["intro"], photo=ui.asset(profile["avatar"]))

# 主要动作
pdf = ui.asset(profile["resume_pdf"])
fields = dict(profile["fields"])
email = fields.get(ui.L({"zh": "邮箱", "en": "Email"}))
col1, col2, col3 = st.columns([1.1, 1, 1])
with col1:
    if pdf:
        st.download_button(f"⬇️  {labels['download']}", pdf.read_bytes(),
                           file_name=pdf.name, mime="application/pdf",
                           use_container_width=True)
with col2:
    if email:
        st.link_button(f"✉️  {labels['send_email']}", f"mailto:{email}",
                       use_container_width=True)
with col3:
    if sd.LINKS.get("github"):
        st.link_button("💻  GitHub", sd.LINKS["github"], use_container_width=True)

ui.section(ui.L({"zh": "关于我", "en": "About me"}))
ui.card("", site["bio"])

ui.section(site["keywords_title"])
ui.chips(site["keywords"])

ui.section(site["now_title"])
ui.bullet_list(site["now"])

ui.section(labels["links_title"])
cols = st.columns(4)
for col, key in zip(cols, ("research", "works", "about", "resume")):
    with col:
        st.page_link(sd.PAGES[key]["file"], label=sd.PAGES[key][ui.lang()])

ui.footer()
