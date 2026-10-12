# -*- coding: utf-8 -*-
"""校验中英两份简历内容的结构是否一致。

中文版 resume_data.py 由 Word 简历同步生成，英文版 resume_data_en.py 手工维护。
中文那边加了条目或改了字段，英文这边没跟上时，本脚本会指出来。

用法：python tools/check_i18n.py
退出码：0 一致；1 不一致（tools/publish.ps1 会据此提示）
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(module_name):
    path = ROOT / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def shape(mod):
    return {
        "PROFILE 字段": list(mod.PROFILE),
        "基本信息条目数": len(mod.PROFILE["fields"]),
        "基本信息每项长度": sorted({len(x) for x in mod.PROFILE["fields"]}),
        "EDUCATION 条数": len(mod.EDUCATION),
        "EDUCATION 字段": sorted({k for item in mod.EDUCATION for k in item}),
        "RESEARCH 条数": len(mod.RESEARCH),
        "RESEARCH 字段": sorted({k for item in mod.RESEARCH for k in item}),
        "HONORS 条数": len(mod.HONORS),
        "SKILLS 条数": len(mod.SKILLS),
        "SUMMARY 类型": type(mod.SUMMARY).__name__,
    }


def main():
    zh = shape(load("resume_data"))
    en = shape(load("resume_data_en"))

    diffs = [(key, zh[key], en[key]) for key in zh if zh[key] != en[key]]

    if not diffs:
        print(f"OK  中英结构一致（教育 {zh['EDUCATION 条数']}｜科研 {zh['RESEARCH 条数']}｜"
              f"荣誉 {zh['HONORS 条数']}｜技能 {zh['SKILLS 条数']}）")
        return 0

    print("中英简历内容结构不一致，请检查 resume_data_en.py：")
    for key, z, e in diffs:
        print(f"  {key}：中文 {z!r} ≠ 英文 {e!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
