# -*- coding: utf-8 -*-
"""页面共用件：语言切换、主题样式、小节标题、侧边栏、页脚。

每个页面按 apply_theme() → sidebar() → 内容 → footer() 的顺序调用即可。
"""
from pathlib import Path

import streamlit as st

import resume_data
import resume_data_en
import site_data as sd

ROOT = Path(__file__).resolve().parent          # 与仓库根、云端工作目录一致
ACCENT = "#284967"                              # 取自简历 PDF 的品牌深蓝
LANGS = ("zh", "en")
LANG_LABELS = {"中文": "zh", "English": "en"}


# ------------------------------------------------------------------ 语言
def bootstrap_lang():
    """入口最开头调用：确定本次运行的语言（URL 参数优先，其次会话状态）。"""
    requested = st.query_params.get("lang")
    if requested in LANGS:
        st.session_state["lang"] = requested
    st.session_state.setdefault("lang", "zh")
    # 让语言开关的控件状态与当前语言保持一致
    st.session_state["lang_choice"] = "中文" if st.session_state["lang"] == "zh" else "English"
    return st.session_state["lang"]


def lang():
    return st.session_state.get("lang", "zh")


def L(mapping):
    """从 {"zh": ..., "en": ...} 里取当前语言的文案。"""
    return mapping[lang()]


def rdata():
    """当前语言对应的简历数据模块。"""
    return resume_data_en if lang() == "en" else resume_data


def asset(rel_path):
    """返回存在的资源路径；缺失返回 None，让页面降级显示而不是报错。"""
    path = ROOT / rel_path
    return path if path.exists() else None


def _switch_lang():
    """语言开关的回调：控件值已在 session_state 里更新，这里只负责切换并重跑。"""
    target = LANG_LABELS.get(st.session_state.get("lang_choice"))
    if target and target != lang():
        st.session_state["lang"] = target
        st.query_params["lang"] = target
        st.rerun()


# ------------------------------------------------------------------ 样式
def apply_theme():
    st.markdown(
        f"""
        <style>
          .brand-bar {{ border-left: 6px solid {ACCENT}; padding: .15rem 0 .15rem .6rem;
                        margin: .2rem 0 .6rem 0; }}
          .brand-bar span {{ font-size: 1.05rem; font-weight: 700; color: {ACCENT};
                             letter-spacing: .06em; }}
          .field-label {{ color: #6b7280; font-size: .82rem; }}
          .field-value {{ font-size: .98rem; }}
          .tag {{ display:inline-block; background:{ACCENT}14; color:{ACCENT};
                  border-radius:999px; padding:.1rem .55rem; margin:.15rem .25rem .15rem 0;
                  font-size:.8rem; }}
          a {{ text-decoration: none; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def heading(text):
    st.markdown(f'<div class="brand-bar"><span>{text}</span></div>', unsafe_allow_html=True)


def tags(items):
    st.markdown("".join(f'<span class="tag">{x}</span>' for x in items), unsafe_allow_html=True)


# ------------------------------------------------------------------ 侧边栏
def sidebar():
    profile = rdata().PROFILE

    with st.sidebar:
        avatar = asset(profile["avatar"])
        if avatar:
            left, mid, right = st.columns([1, 2, 1])
            with mid:
                st.image(str(avatar), width=150)
        else:
            st.info("未找到证件照（assets/avatar.jpg）")

        st.markdown(f"<h3 style='margin:.2rem 0 .6rem 0'>{profile['name']}</h3>",
                    unsafe_allow_html=True)

        fields = dict(profile["fields"])
        email = fields.get(L({"zh": "邮箱", "en": "Email"}))
        if email:
            st.link_button(f"✉️  {L(sd.LABELS)['send_email']}",
                           f"mailto:{email}", use_container_width=True)
        if sd.LINKS.get("github"):
            st.link_button("💻  GitHub", sd.LINKS["github"], use_container_width=True)

        st.divider()
        pdf = asset(profile["resume_pdf"])
        if pdf:
            st.download_button(f"⬇️  {L(sd.LABELS)['download']}", pdf.read_bytes(),
                               file_name=Path(profile["resume_pdf"]).name,
                               mime="application/pdf", use_container_width=True)
        else:
            st.caption("未找到简历 PDF")

        st.caption(f"{L(sd.LABELS)['updated']}{'：' if lang() == 'zh' else ': '}"
                   f"{getattr(rdata(), 'UPDATED', '—')}")

        st.divider()
        st.segmented_control(
            L(sd.LABELS)["lang_label"],
            options=list(LANG_LABELS),
            key="lang_choice",
            on_change=_switch_lang,
        )


# ------------------------------------------------------------------ 页脚
def footer():
    st.divider()
    name = rdata().PROFILE["name"]
    st.caption(L({
        "zh": f"© 2026 {name} · 代码按 PolyForm 非商业许可 1.0.0 授权，内容版权保留",
        "en": f"© 2026 {name} · Code under the PolyForm Noncommercial License 1.0.0; "
              f"personal content all rights reserved",
    }))
