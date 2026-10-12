# -*- coding: utf-8 -*-
"""首页：个人介绍、方向、近况、快捷入口。"""
import streamlit as st

import site_data as sd
import ui

ui.apply_theme()
ui.sidebar()

profile = ui.rdata().PROFILE
site = ui.L(sd.SITE)
labels = ui.L(sd.LABELS)

st.title(site["name"])
st.markdown(site["intro"])

st.markdown(site["bio"])
st.markdown(f"**{site['keywords_title']}**")
ui.tags(site["keywords"])

st.divider()
ui.heading(site["now_title"])
for line in site["now"]:
    st.markdown(f"- {line}")

st.divider()
ui.heading(labels["links_title"])
left, right = st.columns(2)
with left:
    pdf = ui.asset(profile["resume_pdf"])
    if pdf:
        st.download_button(f"⬇️  {labels['download']}", pdf.read_bytes(),
                           file_name=pdf.name, mime="application/pdf",
                           use_container_width=True)
    if sd.LINKS.get("github"):
        st.link_button("💻  GitHub", sd.LINKS["github"], use_container_width=True)
with right:
    for key in ("research", "works", "about"):
        page = sd.PAGES[key]
        st.page_link(page["file"], label=f"{page['icon']}  {page[ui.lang()]}")

ui.footer()
