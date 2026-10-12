# -*- coding: utf-8 -*-
"""高宏曜 · 个人简历网站（Streamlit）

部署：Streamlit Community Cloud，入口文件 streamlit_app.py（仓库根目录）
本地：streamlit run streamlit_app.py

设计约束（与 Streamlit 的运行模型一致）：
* 每次交互都会把整个脚本从头执行一遍，因此本文件是「幂等纯渲染」——
  不使用跨次运行的状态，不在渲染期写文件或发网络请求。
* 只依赖 streamlit 与标准库，云端构建最快、最不容易失败。
"""
from pathlib import Path

import streamlit as st

import resume_data as data

# ---------------------------------------------------------------- 站点配置
GITHUB_URL = "https://github.com/Pseudosalieri/resume"
SHOW_PHONE = True        # 不想在公开页面上展示手机号，改成 False 即可
ACCENT = "#284967"       # 取自简历 PDF 的品牌深蓝

ROOT = Path(__file__).resolve().parent   # 与 Community Cloud 的工作目录（仓库根）一致
PROFILE = data.PROFILE
# 头衔行：只取方向本身，去掉「求职意向：」这类说明性前缀
ROLE = PROFILE["tagline"].split("：", 1)[-1].strip()


def asset(rel_path):
    """返回存在的资源路径，缺失则返回 None（缺文件时页面只降级提示，不报错）。"""
    p = ROOT / rel_path
    return p if p.exists() else None


# ---------------------------------------------------------------- 页面设置
st.set_page_config(
    page_title=f"{PROFILE['name']} · 个人简历",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
      .brand-bar {{ border-left: 6px solid {ACCENT}; padding: .15rem 0 .15rem .6rem;
                    margin: .2rem 0 .6rem 0; }}
      .brand-bar span {{ font-size: 1.05rem; font-weight: 700; color: {ACCENT};
                         letter-spacing: .06em; }}
      .field-label {{ color: #6b7280; font-size: .82rem; }}
      .field-value {{ font-size: .98rem; }}
      .chip {{ display:inline-block; background:{ACCENT}12; color:{ACCENT};
               border:1px solid {ACCENT}33; border-radius:999px;
               padding:.12rem .55rem; margin:.15rem .25rem .15rem 0; font-size:.82rem; }}
      a {{ text-decoration: none; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def heading(text):
    st.markdown(f'<div class="brand-bar"><span>{text}</span></div>', unsafe_allow_html=True)


# ---------------------------------------------------------------- 侧边栏
with st.sidebar:
    avatar = asset(PROFILE["avatar"])
    if avatar:
        left, mid, right = st.columns([1, 2, 1])
        with mid:
            st.image(str(avatar), width=150)
    else:
        st.info("未找到证件照（assets/avatar.jpg）")

    st.markdown(
        f"<h3 style='margin-bottom:0'>{PROFILE['name']}</h3>"
        f"<div style='color:{ACCENT};font-weight:600;margin-bottom:.6rem'>{ROLE}</div>",
        unsafe_allow_html=True,
    )

    fields = dict(PROFILE["fields"])
    email = fields.get("邮箱")
    phone = fields.get("电话")
    homepage = fields.get("个人主页")

    if email:
        st.link_button("✉️  发送邮件", f"mailto:{email}", use_container_width=True)
    if phone and SHOW_PHONE:
        st.link_button("📞  拨打电话", f"tel:{phone}", use_container_width=True)
    if homepage:
        st.link_button("🌐  个人主页", homepage, use_container_width=True)
    if GITHUB_URL:
        st.link_button("💻  GitHub", GITHUB_URL, use_container_width=True)

    st.divider()
    pdf = asset(PROFILE["resume_pdf"])
    if pdf:
        st.download_button("⬇️  下载简历 PDF", pdf.read_bytes(),
                           file_name="高宏曜-简历.pdf", mime="application/pdf",
                           use_container_width=True)
    else:
        st.caption("简历 PDF 未随仓库提供")

    st.caption(f"内容更新：{getattr(data, 'UPDATED', '—')}")


# ---------------------------------------------------------------- 页首
st.title(PROFILE["name"])
st.caption(ROLE)

basic = [("出生年月", fields.get("出生年月")), ("现居城市", fields.get("现居城市")),
         ("学　　历", fields.get("学历"))]
cols = st.columns(3)
for col, (label, value) in zip(cols, basic):
    if value:
        col.markdown(f"<div class='field-label'>{label}</div>"
                     f"<div class='field-value'>{value}</div>", unsafe_allow_html=True)
if email:
    st.markdown(f"<div class='field-label' style='margin-top:.5rem'>联系方式</div>"
                f"<div class='field-value'>{email}"
                + (f" ｜ {phone}" if phone and SHOW_PHONE else "")
                + "</div>", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------------------- 正文标签页
tab_edu, tab_res, tab_honor, tab_skill, tab_about, tab_file = st.tabs(
    ["教育经历", "科研经历", "荣誉奖励", "技能素质", "自我评价", "简历 PDF"]
)

with tab_edu:
    for item in data.EDUCATION:
        heading(f"{item['school']} ｜ {item['degree']}")
        st.caption(item["period"])
        st.markdown(f"**主修课程**：{item['courses'].split('：', 1)[-1]}")

with tab_res:
    for i, item in enumerate(data.RESEARCH):
        heading(item["title"])
        st.caption(f"{item['period']} ｜ {item['role']}")
        st.markdown(item["detail"])
        if i != len(data.RESEARCH) - 1:
            st.divider()

with tab_honor:
    for h in data.HONORS:
        st.markdown(f"- {h}")

with tab_skill:
    for s in data.SKILLS:
        st.markdown(f"- {s}")

with tab_about:
    st.markdown(data.SUMMARY)

with tab_file:
    st.markdown("简历 PDF 与网页内容同源，均为最新版本，可直接下载：")
    if pdf:
        st.download_button("⬇️  下载最新版 PDF", pdf.read_bytes(),
                           file_name="高宏曜-简历.pdf", mime="application/pdf")
    else:
        st.info("未找到简历 PDF")
    st.caption("如需打印或投递，使用这个 PDF 即可。")
