# -*- coding: utf-8 -*-
"""从简历 docx 同步文案到 website/resume_data.py

用途：改完 docx 后，重跑本脚本即可把最新文案同步进网站（本地工具，云端不参与运行）。

用法：
    python website/tools/sync_from_docx.py [docx路径]

默认 docx 路径（相对仓库根）：../高宏曜 研发—理化分析开发方向.docx
依赖：python-docx（仅本地需要：pip install python-docx）
"""
import re
import sys
from pathlib import Path

import docx

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ROOT = Path(__file__).resolve().parent.parent          # website/
DEFAULT_DOCX = ROOT.parent / "高宏曜 研发—理化分析开发方向.docx"
OUT = ROOT / "resume_data.py"

DATE_RE = re.compile(r"^\d{4}\s*年\s*\d{2}\s*月")
BANNERS = ["基本信息", "教育经历", "科研经历", "荣誉奖励", "技能素质", "自我评价"]


def in_textbox(el):
    return any(str(a.tag).endswith("}txbxContent") for a in el.iterancestors())


def row_paragraphs(tr):
    """行内各单元格的段落文本（保持文档顺序，跳过文本框内容）"""
    out = []
    for tc in tr.findall(W + "tc"):
        for p in tc.iter(W + "p"):
            if in_textbox(p):
                continue
            txt = "".join(t.text or "" for t in p.iter(W + "t")).strip()
            if txt:
                out.append(txt)
    return out


def row_is_banner(tr):
    tcs = tr.findall(W + "tc")
    if len(tcs) != 1:
        return None
    tcPr = tcs[0].find(W + "tcPr")
    if tcPr is None or tcPr.find(W + "gridSpan") is None:
        return None
    text = "".join(t.text or "" for t in tcs[0].iter(W + "t"))
    hits = [b for b in BANNERS if b in text]
    return hits[0] if len(hits) == 1 else None


def extract(path):
    d = docx.Document(str(path))
    tbl = d.tables[0]
    sections = {}
    current = None
    for tr in tbl._tbl.findall(W + "tr"):
        banner = row_is_banner(tr)
        if banner:
            current = banner
            sections[current] = []
            continue
        if current:
            sections[current].extend(row_paragraphs(tr))

    full = "".join(
        "".join(t.text or "" for t in p.iter(W + "t"))
        for p in d.element.body.iter(W + "p")
    )

    # ---- 基本信息 ----
    name, fields = None, []
    info = sections["基本信息"]
    for i in range(0, len(info) - 1, 2):
        label, value = info[i], info[i + 1]
        if not label.endswith("："):
            continue
        key = re.sub(r"[\s\u3000]+", "", label.rstrip("："))
        if key == "姓名":
            name = value
        else:
            fields.append((key, value))
    assert name, "未找到姓名"

    # 求职意向（页首文本框里；只取文本框直属段落，避开嵌套文本框的重复文本）
    tagline = None
    for txbx in d.element.body.iter(W + "txbxContent"):
        for p in txbx.findall(W + "p"):
            txt = "".join(t.text or "" for t in p.iter(W + "t")).strip()
            if txt.startswith("求职意向"):
                dup = txt.find("求职意向", 1)          # 去掉被拼接进来的重复片段
                if dup > 0:
                    txt = txt[:dup]
                tagline = txt
                break
        if tagline:
            break
    assert tagline, "未找到求职意向"

    # ---- 教育经历 / 科研经历：按「起始日期」切分条目 ----
    def group(items, keys, tail_prefix):
        entries, cur = [], None
        for s in items:
            if DATE_RE.match(s):
                cur = {"period": s}
                entries.append(cur)
            elif cur is None:
                continue
            else:
                filled = [k for k in keys if k in cur]
                if len(filled) < len(keys) - 1:
                    cur[keys[len(filled)]] = s
                else:
                    cur.setdefault(keys[-1], "")
                    cur[keys[-1]] = (cur[keys[-1]] + " " + s).strip()
        for e in entries:
            assert e[keys[0]] if keys[0] in e else True
        return entries

    education = group(sections["教育经历"], ["period", "school", "degree", "courses"], "主修课程")
    research = group(sections["科研经历"], ["period", "title", "role", "detail"], None)
    for e in education:
        assert set(e) == {"period", "school", "degree", "courses"}, f"教育经历字段不全: {e}"
        assert e["courses"].startswith("主修课程"), e["courses"]
    for r in research:
        assert set(r) == {"period", "title", "role", "detail"}, f"科研经历字段不全: {r}"

    data = {
        "name": name,
        "tagline": tagline,
        "fields": fields,
        "education": education,
        "research": research,
        "honors": sections["荣誉奖励"],
        "skills": sections["技能素质"],
        "summary": " ".join(sections["自我评价"]).strip(),
    }
    return data, full


def py_literal(obj, indent=0):
    pad = " " * indent
    if isinstance(obj, str):
        s = obj.replace("\\", "\\\\").replace('"', '\\"')
        return '"%s"' % s
    if isinstance(obj, tuple):
        return "(" + ", ".join(py_literal(x) for x in obj) + ")"
    if isinstance(obj, list):
        if not obj:
            return "[]"
        items = [py_literal(x, indent + 4) for x in obj]
        inner = ",\n".join(pad + "    " + it for it in items)
        return "[\n" + inner + ",\n" + pad + "]"
    if isinstance(obj, dict):
        inner = ",\n".join(
            pad + '    "%s": %s' % (k, py_literal(v, indent + 4)) for k, v in obj.items()
        )
        return "{\n" + inner + ",\n" + pad + "}"
    raise TypeError(type(obj))


def render(data, src_name):
    import datetime
    updated = datetime.date.today().strftime("%Y-%m-%d")
    return f'''# -*- coding: utf-8 -*-
"""简历内容（网站的唯一文案来源）——直接改本文件即可，改完 git push 网站会自动更新。

初次由 tools/sync_from_docx.py 从「{src_name}」逐字提取生成；
若 docx 又改了，可重跑该脚本覆盖本文件（本地工具，云端不参与运行）。
"""

UPDATED = {py_literal(updated)}

PROFILE = {{
    "name": {py_literal(data["name"])},
    "tagline": {py_literal(data["tagline"])},
    "avatar": "assets/avatar.jpg",
    "fields": {py_literal(data["fields"], 4)},
}}

EDUCATION = {py_literal(data["education"])}

RESEARCH = {py_literal(data["research"])}

HONORS = {py_literal(data["honors"])}

SKILLS = {py_literal(data["skills"])}

SUMMARY = {py_literal(data["summary"])}
'''


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DOCX
    if not src.exists():
        sys.exit(f"找不到 docx：{src}")
    data, full = extract(src)
    OUT.write_text(render(data, src.name), encoding="utf-8")

    # ---- 断言：把刚写出的文件 exec 一遍，逐条核对确实来自 docx 原文 ----
    ns = {}
    exec(compile(OUT.read_text(encoding="utf-8"), str(OUT), "exec"), ns)
    norm = re.sub(r"\s+", "", full)
    flat = []

    def walk(o):
        if isinstance(o, str):
            flat.append(o)
        elif isinstance(o, (list, tuple)):
            for x in o:
                walk(x)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)

    for k in ("EDUCATION", "RESEARCH", "HONORS", "SKILLS", "SUMMARY"):
        walk(ns[k])
    walk(ns["PROFILE"]["fields"])
    flat += [ns["PROFILE"]["name"], ns["PROFILE"]["tagline"]]

    texts = [s for s in flat if len(s) > 1 and not s.endswith(".pdf")]
    missing = [s for s in texts if re.sub(r"\s+", "", s) not in norm]
    assert not missing, "以下文案在 docx 原文中找不到：\n" + "\n".join(missing[:5])
    print(f"OK  已生成 {OUT}")
    print(f"    来源：{src}")
    print(f"    条目：教育 {len(ns['EDUCATION'])}｜科研 {len(ns['RESEARCH'])}｜"
          f"荣誉 {len(ns['HONORS'])}｜技能 {len(ns['SKILLS'])}｜基本信息 {len(ns['PROFILE']['fields'])}")
    print(f"    逐字一致性校验：{len(texts)} 条文案全部命中文档原文")


if __name__ == "__main__":
    main()
