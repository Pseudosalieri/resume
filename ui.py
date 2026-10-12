# -*- coding: utf-8 -*-
"""页面共用件：设计系统（CSS）、语言、侧边栏、卡片等构件。

页面按 apply_theme() → sidebar() → 内容 → footer() 的顺序调用。
样式全部基于实测到的 data-testid 选择器，不依赖 Streamlit 的随机类名。
"""
import html
from pathlib import Path

import streamlit as st

import resume_data
import resume_data_en
import site_data as sd

ROOT = Path(__file__).resolve().parent          # 与仓库根、云端工作目录一致
ACCENT = "#284967"
ACCENT_SOFT = "#eef2f7"
INK = "#1f2937"
MUTED = "#6b7280"
LINE = "#e6e8ec"
LANGS = ("zh", "en")
LANG_LABELS = {"中文": "zh", "English": "en"}

CSS = f"""
:root {{
  --accent: {ACCENT}; --accent-soft: {ACCENT_SOFT};
  --ink: {INK}; --muted: {MUTED}; --line: {LINE};
}}
html, body, [data-testid="stAppViewContainer"] {{ background: #fcfcfd; }}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stToolbar"] {{ right: .6rem; }}

/* 正文容器：限宽居中，收紧默认的夸张留白 */
[data-testid="stMainBlockContainer"] {{
  max-width: 900px; padding: 2.2rem 1.6rem 3rem 1.6rem; margin: 0 auto;
}}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {{ line-height: 1.8; color: #374151; }}

/* 侧边栏：只改配色与导航样式，不动它的宽度和布局 */
[data-testid="stSidebar"] {{
  background: #ffffff; border-right: 1px solid var(--line);
}}
[data-testid="stSidebarNav"] {{ padding: .4rem .7rem .2rem; }}
[data-testid="stNavSectionHeader"] {{
  font-size: .68rem; letter-spacing: .14em; text-transform: uppercase;
  color: #9aa3af; font-weight: 600; margin: .9rem .4rem .3rem;
}}
[data-testid="stSidebarNavLink"] {{
  border-radius: 9px; padding: .34rem .5rem; color: #374151; font-size: .9rem;
}}
[data-testid="stSidebarNavLink"]:hover {{ background: var(--accent-soft); color: var(--accent); }}
[data-testid="stSidebarNavLink"][aria-current="page"] {{
  background: var(--accent-soft); color: var(--accent); font-weight: 600;
}}

/* 头像 */
[data-testid="stImage"] img {{
  border-radius: 16px; border: 1px solid var(--line);
  box-shadow: 0 4px 18px rgba(31, 41, 55, .08);
}}

/* 按钮 / 链接按钮 / 下载按钮：统一成轻量胶囊 */
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseLinkButton-secondary"] {{
  border: 1px solid var(--line); background: #fff; color: var(--ink);
  border-radius: 10px; padding: .42rem .9rem; font-size: .88rem; font-weight: 500;
  box-shadow: none; transition: all .15s ease; min-height: 0;
}}
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseLinkButton-secondary"]:hover {{
  border-color: var(--accent); color: var(--accent);
  background: var(--accent-soft); transform: translateY(-1px);
}}

/* 页内链接：做成卡片式的入口 */
[data-testid="stPageLink-NavLink"] {{
  border: 1px solid var(--line); background: #fff; border-radius: 11px;
  padding: .55rem .75rem; font-size: .9rem; transition: all .15s ease;
  display: block; width: 100%; text-align: center; box-sizing: border-box;
}}
[data-testid="stPageLink-NavLink"]:hover {{
  border-color: var(--accent); background: var(--accent-soft);
  color: var(--accent); transform: translateY(-1px);
}}

/* 语言开关 */
[data-testid="stButtonGroup"] button {{
  border-radius: 8px; font-size: .82rem; padding: .18rem .6rem;
}}
[data-testid="stWidgetLabel"] p {{ font-size: .78rem; color: var(--muted); }}

/* ---- 自定义构件 ---- */
.hero {{ padding: .2rem 0 .4rem; }}
.hero h1 {{
  font-size: 2.3rem; line-height: 1.15; margin: 0 0 .5rem;
  letter-spacing: -.02em; color: var(--ink); font-weight: 700;
}}
.hero .role {{ color: var(--accent); font-weight: 600; font-size: 1rem; margin-bottom: .7rem; }}
.hero .intro {{ color: #374151; font-size: 1.02rem; line-height: 1.85; margin-bottom: .2rem; }}

.sec {{ display: flex; align-items: center; gap: .55rem; margin: 1.9rem 0 .8rem; }}
.sec .bar {{ width: 4px; height: 17px; border-radius: 2px; background: var(--accent); }}
.sec .txt {{ font-weight: 600; color: var(--ink); letter-spacing: .04em; font-size: 1rem; }}

.card {{
  border: 1px solid var(--line); background: #fff; border-radius: 14px;
  padding: 1rem 1.15rem; margin-bottom: .7rem; transition: all .18s ease;
}}
.card:hover {{ box-shadow: 0 4px 20px rgba(40, 73, 103, .09); border-color: #d9dfe7; }}
.card h3 {{ font-size: 1.02rem; margin: 0 0 .3rem; color: var(--ink); font-weight: 650; }}
.card .meta {{ color: var(--muted); font-size: .82rem; margin-bottom: .5rem; }}
.card .body {{ color: #374151; font-size: .94rem; line-height: 1.85; }}
.card .body p {{ margin: 0 0 .5rem; }}

.chips {{ margin: .1rem 0 .2rem; }}
.chip {{
  display: inline-block; background: var(--accent-soft); color: var(--accent);
  border-radius: 999px; padding: .22rem .68rem; margin: .18rem .3rem .18rem 0;
  font-size: .8rem; font-weight: 500;
}}

.timeline-item {{
  border-left: 2px solid var(--line); padding: .1rem 0 .9rem 1rem;
  position: relative; margin-left: .3rem;
}}
.timeline-item::before {{
  content: ""; position: absolute; left: -6.5px; top: .45rem; width: 11px; height: 11px;
  border-radius: 50%; background: #fff; border: 2px solid var(--accent);
}}
.timeline-item:last-child {{ padding-bottom: .2rem; }}
.timeline-item .when {{ color: var(--muted); font-size: .8rem; }}
.timeline-item .what {{ font-weight: 600; color: var(--ink); font-size: .97rem; margin: .15rem 0 .2rem; }}
.timeline-item .detail {{ color: #374151; font-size: .9rem; line-height: 1.7; }}

.plain-list {{ margin: 0; padding-left: 1.05rem; }}
.plain-list li {{ color: #374151; font-size: .93rem; line-height: 1.75; margin-bottom: .3rem; }}

.contact-line {{ display: flex; gap: .6rem; align-items: baseline; margin-bottom: .45rem; }}
.contact-line .k {{ color: var(--muted); font-size: .8rem; min-width: 4.2rem; }}
.contact-line .v {{ color: var(--ink); font-size: .93rem; word-break: break-all; }}

.side-name {{ font-size: 1.06rem; font-weight: 650; color: var(--ink); text-align: center; margin: .6rem 0 .1rem; }}
.side-role {{ font-size: .8rem; color: var(--muted); text-align: center; margin-bottom: .2rem; }}
.side-links {{ display: flex; flex-direction: column; gap: .25rem; margin-top: .5rem; }}
.side-links a {{ color: #374151; font-size: .86rem; padding: .3rem .45rem; border-radius: 8px; }}
.side-links a:hover {{ background: var(--accent-soft); color: var(--accent); }}
.foot {{ color: #9aa3af; font-size: .76rem; line-height: 1.7; }}
"""


# ------------------------------------------------------------------ 语言
def bootstrap_lang():
    """入口最开头调用：确定本次运行的语言（URL 参数优先，其次会话状态）。"""
    requested = st.query_params.get("lang")
    if requested in LANGS:
        st.session_state["lang"] = requested
    st.session_state.setdefault("lang", "zh")
    st.session_state["lang_choice"] = "中文" if st.session_state["lang"] == "zh" else "English"
    return st.session_state["lang"]


def lang():
    return st.session_state.get("lang", "zh")


def L(mapping):
    return mapping[lang()]


def rdata():
    return resume_data_en if lang() == "en" else resume_data


def asset(rel_path):
    path = ROOT / rel_path
    return path if path.exists() else None


def _switch_lang():
    target = LANG_LABELS.get(st.session_state.get("lang_choice"))
    if target and target != lang():
        st.session_state["lang"] = target
        st.query_params["lang"] = target
        st.rerun()


# ------------------------------------------------------------------ 样式与构件
def apply_theme():
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def esc(value):
    return html.escape(str(value))


def hero(name, intro, role="", photo=None):
    """页首：左侧姓名与介绍，右侧证件照（有照片时）。"""
    left, right = st.columns([2.7, 1], vertical_alignment="center")
    with right:
        if photo:
            st.image(str(photo), width=150)
    with left:
        role_html = f'<div class="role">{esc(role)}</div>' if role else ""
        st.markdown(
            f'<div class="hero"><h1>{esc(name)}</h1>{role_html}'
            f'<div class="intro">{esc(intro)}</div></div>',
            unsafe_allow_html=True,
        )


def page_title(text):
    st.markdown(f'<div class="hero"><h1 style="font-size:1.9rem">{esc(text)}</h1></div>',
                unsafe_allow_html=True)


def section(label):
    st.markdown(
        f'<div class="sec"><div class="bar"></div><div class="txt">{esc(label)}</div></div>',
        unsafe_allow_html=True,
    )


def card(title, body="", meta="", tags=None):
    parts = [f'<div class="card">']
    if title:
        parts.append(f"<h3>{esc(title)}</h3>")
    if meta:
        parts.append(f'<div class="meta">{esc(meta)}</div>')
    if body:
        paragraphs = "".join(f"<p>{esc(p)}</p>" for p in str(body).split("\n") if p.strip())
        parts.append(f'<div class="body">{paragraphs}</div>')
    if tags:
        parts.append(chips_html(tags))
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def chips_html(items):
    return '<div class="chips">' + "".join(f'<span class="chip">{esc(x)}</span>'
                                           for x in items) + "</div>"


def chips(items):
    st.markdown(chips_html(items), unsafe_allow_html=True)


def bullet_list(items):
    st.markdown('<ul class="plain-list">'
                + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>",
                unsafe_allow_html=True)


def timeline(items):
    """items: [(when, what, detail), ...]"""
    rows = []
    for when, what, detail in items:
        rows.append(
            f'<div class="timeline-item"><div class="when">{esc(when)}</div>'
            f'<div class="what">{esc(what)}</div>'
            + (f'<div class="detail">{esc(detail)}</div>' if detail else "")
            + "</div>"
        )
    st.markdown("".join(rows), unsafe_allow_html=True)


def contact_lines(pairs):
    rows = "".join(f'<div class="contact-line"><div class="k">{esc(k)}</div>'
                   f'<div class="v">{esc(v)}</div></div>' for k, v in pairs if v)
    st.markdown(rows, unsafe_allow_html=True)


# ------------------------------------------------------------------ 侧边栏
def sidebar():
    profile = rdata().PROFILE
    labels = L(sd.LABELS)

    with st.sidebar:
        fields = dict(profile["fields"])
        email = fields.get(L({"zh": "邮箱", "en": "Email"}))
        links = []
        if email:
            links.append(f'<a href="mailto:{esc(email)}">✉️&nbsp; {esc(email)}</a>')
        if sd.LINKS.get("github"):
            links.append(f'<a href="{esc(sd.LINKS["github"])}" target="_blank">💻&nbsp; GitHub</a>')
        if links:
            st.markdown('<div class="side-links">' + "".join(links) + "</div>",
                        unsafe_allow_html=True)

        pdf = asset(profile["resume_pdf"])
        if pdf:
            st.download_button(f"⬇️  {labels['download']}", pdf.read_bytes(),
                               file_name=pdf.name, mime="application/pdf",
                               use_container_width=True)

        st.caption(f"{labels['updated']}{'：' if lang() == 'zh' else ': '}"
                   f"{getattr(rdata(), 'UPDATED', '—')}")

        st.segmented_control(labels["lang_label"], options=list(LANG_LABELS),
                             key="lang_choice", on_change=_switch_lang)


# ------------------------------------------------------------------ 页脚
def footer():
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="foot">' + esc(L({
            "zh": "© 2026 高宏曜　·　代码按 PolyForm 非商业许可 1.0.0 授权，"
                  "证件照与简历文案版权保留",
            "en": "© 2026 Hongyao Gao　·　Code under the PolyForm Noncommercial "
                  "License 1.0.0; photograph and résumé text all rights reserved",
        })) + "</div>",
        unsafe_allow_html=True,
    )
