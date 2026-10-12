# -*- coding: utf-8 -*-
"""关于我：教育经历、荣誉奖励、技能素质、自我评价。内容逐字来自 Word 简历。"""
import re

import streamlit as st

import site_data as sd
import ui

ui.apply_theme()
ui.sidebar()

labels = ui.L(sd.LABELS)
data = ui.rdata()

# 技能条目在简历里带 ①②③ 序号，页面上去掉
_MARKER = re.compile(r"^\s*[①-⑳]\s*")


def strip_marker(text):
    return _MARKER.sub("", text).strip()


st.title(sd.PAGES["about"][ui.lang()])

ui.heading(labels["education"])
for item in data.EDUCATION:
    st.markdown(f"**{item['school']}**　{item['degree']}")
    st.caption(item["period"])
    courses = item["courses"].split("：", 1)[-1]
    st.markdown(f"{labels['courses']}：{courses}")
    st.write("")

ui.heading(labels["honors"])
for honor in data.HONORS:
    st.markdown(f"- {honor}")

st.write("")
ui.heading(labels["skills"])
for skill in data.SKILLS:
    st.markdown(f"- {strip_marker(skill)}")

st.write("")
ui.heading(labels["summary"])
st.markdown(data.SUMMARY)

ui.footer()
