# 高宏曜的个人主页

线上地址：<https://gaohongyao-resume.streamlit.app/>

用 Streamlit 写的单页站点，目前内容主要是简历：教育经历、科研经历、荣誉奖励、技能素质、
自我评价，外加一份 PDF 下载。页面上的文字不是手敲的，是从 Word 版简历同步过来的，
省得同一份内容维护两处。

部署在 Streamlit Community Cloud（免费）。GitHub 这边只管存代码，push 之后云端自动
拉去重建，通常一分钟内生效。

## 改内容

改完 Word 简历（`../高宏曜 研发—理化分析开发方向.docx`）以后，在仓库根目录跑：

```powershell
.\tools\publish.ps1
```

脚本做三件事：把简历文案逐字提取出来重写 `resume_data.py`；调本机 Word 重新导出最新的一页
PDF 覆盖 `assets/高宏曜-简历.pdf`；提交并推送。所以页面上看到的和下载到的永远是同一版。

跑之前确认本机装了 Word。`python-docx` 如果缺，脚本会自己装进 `.venv`。简历要是超过一页，
脚本会提醒一句。

只想改网页文字、不动 PDF，那就直接改 `resume_data.py`，然后正常 commit、push。
换证件照：新照片存成 `assets/avatar.jpg`（竖版，360×504 以上就够），push。

## 本地跑

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

得在仓库根目录执行。云端的工作目录就是仓库根，本地保持一致，路径解析出来的结果才一样。

## 文件

```
streamlit_app.py          入口，部署时的主文件填这个
resume_data.py            页面上的文字都来自这里
tools/publish.ps1         一键同步：文案 + PDF + 提交推送
tools/sync_from_docx.py   publish.ps1 调用的提取脚本，也能单独跑
assets/avatar.jpg         证件照
assets/高宏曜-简历.pdf      页面上提供下载的就是这一份
.streamlit/config.toml    主题色，必须放仓库根目录，否则云端不读
.devcontainer/            Dev Container / Codespaces 配置
requirements.txt          锁了 streamlit==1.65.0，和本地验证过的版本一致
```

## 重新部署

share.streamlit.io → Create app → 选 "Yup, I have an app" → 点 "Paste GitHub URL"，粘
`https://github.com/Pseudosalieri/resume/blob/main/streamlit_app.py`，仓库、分支、主文件
三项会自动填好。App URL 那栏填 `gaohongyao-resume`，不填会生成一长串很难记的子域名。

Advanced settings 里的 Python 版本选 3.12。这个选了之后不能再改，要换只能把应用删掉重新部署。

部署流程本身是照 [这篇](https://vocus.cc/article/69af99cefd89780001bfb6f0) 走的。

## 踩过的坑

`st.pdf` 用不了。它依赖可选组件 `streamlit-pdf`，但 2.1.0 版跟 Streamlit 1.65 的组件机制
对不上，导入直接抛 `StreamlitAPIException`，所以没做内嵌预览，只给下载。

免费版应用 12 小时没人访问就休眠，访客得点一下按钮唤醒。想让它一直醒着，可以拿 UptimeRobot
这类免费监控每隔几分钟 ping 一次。

应用默认是公开的，每周还会被搜索引擎抓一遍。页面上的手机号如果不想公开，把
`streamlit_app.py` 里的 `SHOW_PHONE` 改成 `False`。

图片、PDF 这类路径按仓库根目录解析，并且只能用 `/`。入口文件就在根目录，所以
`Path(__file__).parent` 正好等于仓库根；以后要是挪目录，记得这一条。

仓库改名的话，`streamlit_app.py` 里的 `GITHUB_URL` 和上面那条部署链接要一起改。
