# -*- coding: utf-8 -*-
"""高宏曜的个人网站 —— 入口文件。

页面与导航在下面按 site_data.NAV 声明，各页面的内容在 views/ 目录里。
部署：Streamlit Community Cloud，主文件填 streamlit_app.py；本地：streamlit run streamlit_app.py
"""
import streamlit as st

import site_data as sd
import ui

# 语言必须在建导航之前定下来，导航标签才能跟着切换
ui.bootstrap_lang()

st.set_page_config(
    page_title=ui.rdata().PROFILE["name"],
    page_icon="🧪",
    layout="wide",            # 宽度由 ui.CSS 里的 stMainBlockContainer 限制并居中
    initial_sidebar_state="expanded",
)


def build_page(key):
    page = sd.PAGES[key]
    label = page[ui.lang()]
    # 用 emoji 而不是 Material 图标：后者靠 Google Fonts 的连字渲染，
    # 在字体拉不到的网络环境（例如中国大陆）会退化成 "home" 这样的英文单词。
    icon = page["icon"]
    if key == "github":                       # 外链，点击在新标签打开
        return st.Page(sd.LINKS["github"], title=label, icon=icon)
    if key == "home":
        return st.Page(page["file"], title=label, icon=icon, default=True)
    return st.Page(page["file"], title=label, icon=icon)


navigation = {
    section: [build_page(key) for key in keys]
    for section, keys in sd.NAV[ui.lang()].items()
}

st.navigation(navigation).run()
