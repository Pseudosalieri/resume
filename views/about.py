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
_MARKER = re.compile(r"^\s*[①-⑳]\s*")

ui.page_title(sd.PAGES["about"][ui.lang()])

ui.section(labels["education"])
ui.timeline([
    (item["period"], f"{item['school']}　{item['degree']}",
     f"{labels['courses']}：{item['courses'].split('：', 1)[-1]}")
    for item in data.EDUCATION
])

ui.section(labels["honors"])
ui.bullet_list(data.HONORS)

ui.section(labels["skills"])
ui.bullet_list([_MARKER.sub("", s).strip() for s in data.SKILLS])

ui.section(labels["summary"])
ui.card("", data.SUMMARY)

ui.footer()
