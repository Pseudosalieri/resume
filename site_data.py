# -*- coding: utf-8 -*-
"""站点级内容（与简历无关的那部分）：首页文案、作品、导航、界面文字、外链。

改站点的门面文字就改这里，改完 push 即生效。
简历正文不在这里，中文来自 resume_data.py（由 Word 简历同步），英文在 resume_data_en.py。

双语约定：凡是需要翻译的内容都写成 {"zh": ..., "en": ...}，页面用 ui.L(...) 取当前语言。
"""

# 是否在页面上展示手机号（想隐藏就改成 False）
SHOW_PHONE = True

# 站外链接（两种语言共用）
LINKS = {
    "github": "https://github.com/Pseudosalieri/resume",
    "thesis_refinery": "https://github.com/Pseudosalieri/thesis-refinery",
}

SITE = {
    "zh": {
        "name": "高宏曜",
        # 首页一句话定位，刻意不写求职意向
        "intro": "药学硕士在读，做多肽固相合成与色谱分析，业余用 AI 写点本地小工具。",
        "bio": "目前在沈阳药科大学读药学硕士。手上的活主要围绕多肽固相合成、HPLC 分析与制备纯化，"
               "以及小分子化合物的合成和谱图解析。实验之外喜欢把重复的事交给脚本——比如把学位论文的"
               "排版流程自动化，或者用 reveal.js 把汇报做成能点的网页。",
        "keywords_title": "方向",
        "keywords": ["多肽固相合成", "HPLC 方法开发", "制备纯化", "NMR / MS 谱图解析"],
        "now_title": "近况",
        "now": [
            "沈阳药科大学 药学硕士在读，预计 2027 年 06 月毕业",
            "课题：白斑综合征病毒 VP15 抗原肽的合成与纯化工艺；吲哚类 ATX 抑制剂的设计合成与构效关系",
        ],
    },
    "en": {
        "name": "Hongyao Gao",
        "intro": "M.Sc. student in pharmacy. I work on solid-phase peptide synthesis and "
                 "chromatographic analysis, and build small local tools with AI on the side.",
        "bio": "I'm a master's student in pharmacy at Shenyang Pharmaceutical University. Most of "
               "my bench work is solid-phase peptide synthesis, HPLC analysis and preparative "
               "purification, plus the synthesis and spectral characterisation of small molecules. "
               "Outside the lab I tend to automate the repetitive parts — formatting my thesis with "
               "a script, or turning presentations into interactive pages with reveal.js.",
        "keywords_title": "Focus",
        "keywords": ["Solid-phase peptide synthesis", "HPLC method development",
                     "Preparative purification", "NMR / MS interpretation"],
        "now_title": "Now",
        "now": [
            "M.Sc. in Pharmacy, Shenyang Pharmaceutical University (expected Jun 2027)",
            "Topics: synthesis and purification process of WSSV VP15 antigen peptides; design, "
            "synthesis and SAR of indole-based ATX inhibitors",
        ],
    },
}

# 作品。detail 留空就先不显示；link 是外链，link_label 是链接文字（留空则显示网址）。
WORKS = {
    "zh": [
        {"title": "学位论文排版与精修",
         "summary": "把已经写成的 Word 学位论文变成可复现的构建产物：版式与校验都由命令完成，"
                    "用断言而不是肉眼证明排版没有走样。",
         "detail": "", "link": LINKS["thesis_refinery"], "link_label": "GitHub 仓库",
         "tags": ["Python", "Quarto", "开源"]},
        {"title": "可交互 HTML 学术汇报",
         "summary": "基于 reveal.js 制作可交互的学术汇报演示文稿。",
         "detail": "", "tags": ["reveal.js", "HTML"]},
        {"title": "本站：Streamlit 个人网站",
         "summary": "用 Streamlit 写的个人网站，托管在 Streamlit Community Cloud，"
                    "页面文字由 Word 文档自动同步生成。",
         "detail": "", "tags": ["Streamlit", "Python"]},
    ],
    "en": [
        {"title": "Thesis formatting and copy-editing",
         "summary": "Turns an already-written Word thesis into a reproducible build artifact: "
                    "the format pass and the checks run from the command line, so assertions, "
                    "not eyeballs, prove the layout did not drift.",
         "detail": "", "link": LINKS["thesis_refinery"], "link_label": "GitHub repository",
         "tags": ["Python", "Quarto", "open source"]},
        {"title": "Interactive HTML presentations",
         "summary": "Academic presentations built with reveal.js, so slides can be clicked through "
                    "in a browser.",
         "detail": "", "tags": ["reveal.js", "HTML"]},
        {"title": "This site: a Streamlit personal website",
         "summary": "A personal site written in Streamlit and hosted on Streamlit Community Cloud; "
                    "the page text is generated from a Word document.",
         "detail": "", "tags": ["Streamlit", "Python"]},
    ],
}

# 导航：分组标题 -> 页面 key（顺序即显示顺序）。"" 表示不分组。
NAV = {
    "zh": {"": ["home"], "内容": ["research", "works", "about"], "其它": ["contact", "github"]},
    "en": {"": ["home"], "Content": ["research", "works", "about"], "Other": ["contact", "github"]},
}

# 页面清单：key -> 文件、两种语言的标签、导航图标（Material Symbols）、备用 emoji。
# github 走外链，没有文件。
PAGES = {
    "home":     {"file": "views/home.py",     "zh": "首页",      "en": "Home",
                 "material": ":material/home:",       "icon": "🏠"},
    "research": {"file": "views/research.py", "zh": "科研与项目", "en": "Research",
                 "material": ":material/science:",    "icon": "🔬"},
    "works":    {"file": "views/works.py",    "zh": "作品",      "en": "Works",
                 "material": ":material/widgets:",    "icon": "🧰"},
    "about":    {"file": "views/about.py",    "zh": "关于我",    "en": "About",
                 "material": ":material/person:",     "icon": "📄"},
    "contact":  {"file": "views/contact.py",  "zh": "联系",      "en": "Contact",
                 "material": ":material/mail:",       "icon": "✉️"},
    "github":   {"file": "",                  "zh": "GitHub",    "en": "GitHub",
                 "material": ":material/code:",       "icon": "💻"},
}

# 界面文字
LABELS = {
    "zh": {
        "send_email": "发送邮件",
        "contact_title": "联系方式",
        "updated": "内容更新",
        "education": "教育经历",
        "honors": "荣誉奖励",
        "skills": "技能素质",
        "summary": "自我评价",
        "courses": "主修课程",
        "role_at": "担任",
        "lang_label": "语言",
    },
    "en": {
        "send_email": "Email me",
        "contact_title": "Contact",
        "updated": "Updated",
        "education": "Education",
        "honors": "Honours & awards",
        "skills": "Skills",
        "summary": "Summary",
        "courses": "Core courses",
        "role_at": "Role",
        "lang_label": "Language",
    },
}
