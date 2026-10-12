# -*- coding: utf-8 -*-
"""联系：邮箱、GitHub、电话（受 site_data.SHOW_PHONE 控制）等。"""
import streamlit as st

import site_data as sd
import ui

ui.apply_theme()
ui.sidebar()

labels = ui.L(sd.LABELS)
fields = dict(ui.rdata().PROFILE["fields"])
pick = lambda zh_key, en_key: fields.get(zh_key if ui.lang() == "zh" else en_key)

ui.page_title(sd.PAGES["contact"][ui.lang()])

pairs = [
    (ui.L({"zh": "邮箱", "en": "Email"}), pick("邮箱", "Email")),
    (ui.L({"zh": "现居城市", "en": "Location"}), pick("现居城市", "Location")),
]
if sd.SHOW_PHONE:
    pairs.append((ui.L({"zh": "电话", "en": "Phone"}), pick("电话", "Phone")))

ui.contact_lines(pairs)

email = pick("邮箱", "Email")
if email:
    st.link_button(f"✉️  {labels['send_email']}", f"mailto:{email}")
if sd.LINKS.get("github"):
    st.link_button("💻  GitHub", sd.LINKS["github"])

ui.footer()
