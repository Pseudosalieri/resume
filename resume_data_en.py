# -*- coding: utf-8 -*-
"""英文版简历内容。

结构与 resume_data.py（中文版，由 Word 简历同步生成）严格一致：
同样的键、同样的条目数、同样的元组长度。改动中文内容后如果条目数变了，
tools/check_i18n.py 会报出结构不一致，tools/publish.ps1 也会提示你回来同步这里。

内容是对中文版既有事实的翻译，不额外添加信息。
"""

UPDATED = "2026-10-12"

PROFILE = {
    "name": "Hongyao Gao",
    "tagline": "",          # 站上不展示，保留字段以对齐中文版结构
    "avatar": "assets/avatar.jpg",
    "fields": [
        ("Date of birth", "2002-01"),
        ("Location", "Weihai, Shandong, China"),
        ("Degree", "M.Sc."),
        ("Email", "ghy11111010010@foxmail.com"),
        ("Phone", "18641369709"),
        ("Homepage", "https://www.example.com"),
    ],
}

EDUCATION = [
    {
        "period": "Sep 2024 – Jun 2027",
        "school": "Shenyang Pharmaceutical University",
        "degree": "Pharmacy (M.Sc.)",
        "courses": "Core courses: chromatographic analysis, advanced organic chemistry, spectral "
                   "interpretation of organic compounds, research design and thesis writing, "
                   "computers in pharmacy.",
    },
    {
        "period": "Sep 2020 – Jun 2024",
        "school": "Shenyang Pharmaceutical University",
        "degree": "Pharmacy (B.Sc.)",
        "courses": "Core courses: analytical chemistry, instrumental analysis, pharmaceutical "
                   "analysis, organic chemistry, medicinal chemistry, spectroscopy, experimental "
                   "design and data analysis.",
    },
]

RESEARCH = [
    {
        "period": "Jun 2026 – Sep 2026",
        "title": "Process development for solid-phase synthesis and purification of WSSV VP15 antigen peptides",
        "role": "Research Assistant",
        "detail": "Worked on the antigenic domain of VP15, the nucleocapsid protein of white spot "
                  "syndrome virus. Took part in designing candidate antigen peptides derived from "
                  "VP15, and independently carried out solid-phase peptide synthesis, resin cleavage "
                  "and work-up. Developed purity analysis and preparative purification methods on an "
                  "analytical HPLC system, completed purification and content assays, and produced "
                  "sufficient lyophilised powder at over 95% purity to support downstream activity "
                  "screening and druggability assessment, helping move an aquatic green antiviral "
                  "formulation towards application.",
    },
    {
        "period": "Sep 2025 – Jun 2026",
        "title": "Design, synthesis and structure–activity relationship study of novel indole-based ATX inhibitors",
        "role": "Research Assistant",
        "detail": "Starting from a lead compound found previously in the group and the structure of "
                  "the ATX inhibitor ziritaxestat, designed and synthesised 21 candidate indole "
                  "derivatives against ATX. Independently ran purity checks and submitted samples for "
                  "1H-NMR, 13C-NMR and MS, then interpreted the spectra; handled data archiving and "
                  "early physicochemical assessment of the compound library, keeping a small-molecule "
                  "record that follows medicinal chemistry practice. Enzymatic and in vitro "
                  "anti-proliferation assays identified candidates with nanomolar IC50 and activity "
                  "comparable to a clinical positive control; molecular docking and PK tools were used "
                  "to model binding at the target and explain the structure–activity relationship, "
                  "pointing to clear directions for optimising the next round of scaffolds.",
    },
]

HONORS = [
    "Shenyang Pharmaceutical University: First-class academic scholarship (2×) and second-class (3×)",
    "Second prize, provincial round, 1st SFLEP·Cihda Cup National College English Vocabulary Contest",
    "First prize, 2022 Liaoning Provincial College Student Plant and Animal Specimen Making Contest",
    "Second prize, science exploration category, 3rd Liaoning Provincial College Student Life Science Innovation and Entrepreneurship Contest",
    "First prize, 2nd Pharmacy Forum for College Students, Shenyang Pharmaceutical University",
    "Outstanding poster award, Liaoning Provincial Undergraduate Pharmacy Forum",
]

SKILLS = [
    "English: CET-6",
    "Confident with ChemDraw, MestReNova, Discovery Studio and similar professional software",
    "Can independently operate UV-Vis and fluorescence spectrophotometers, microplate readers, and HPLC analytical and preparative systems; able to interpret LC-MS/HRMS data submitted for testing. Have run 1H-NMR on a Bruker 400 MHz spectrometer under supervision and can carry out initial interpretation of the spectra",
    "Familiar with searching academic literature, patents and related databases; strong at organising and analysing information",
    "Can build small local AI-assisted applications — for example scripting the formatting and copy-editing of a thesis, or interactive HTML academic presentations with reveal.js",
]

SUMMARY = "Pharmacy background with hands-on experience in solid-phase peptide synthesis, HPLC " \
          "analysis and preparative purification, and MS/NMR spectral interpretation; careful " \
          "about lab records, data archiving and documented procedures. Optimistic and practical, " \
          "with a strong sense of responsibility and good at picking up new things. Uses " \
          "AI-assisted programming to build small local tools that make research work faster. " \
          "Down to earth and collaborative, and keen to apply analytical development skills to " \
          "drug development and quality control while continuing to learn on the job."
