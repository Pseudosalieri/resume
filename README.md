# 高宏曜的个人主页

线上地址：<https://gaohongyao-homepage.streamlit.app/>

用 Streamlit 写的个人网站，中英双语，用侧边栏导航分了几页：

| 页面 | 路径 | 内容 |
| --- | --- | --- |
| 首页 | `/` | 一段自我介绍、方向关键词、近况 |
| 科研与项目 | `/research` | 两段科研经历 |
| 作品 | `/works` | 做过的小东西，能点进代码仓库 |
| 关于我 | `/about` | 教育经历、荣誉奖励、技能素质、自我评价 |
| 联系 | `/contact` | 邮箱、GitHub、电话 |

站上不提供简历下载，页面内容就是全部。页面文字不是手敲的，是从 Word 版简历同步过来的，
省得同一份内容维护两处。英文版是对应内容的翻译，放在单独的文件里手工维护。

部署在 Streamlit Community Cloud（免费）。GitHub 这边只管存代码，push 之后云端自动
拉去重建，通常一分钟内生效。

## 改内容

分三种情况，别搞混：

**改 Word 简历（教育、科研、荣誉、技能、自我评价这些）** —— 在仓库根目录跑：

```powershell
.\tools\publish.ps1
```

脚本做三件事：把简历文案逐字提取出来重写 `resume_data.py`；调本机 Word 重新导出最新的一页
PDF 覆盖 `assets/高宏曜-简历.pdf`（这份只是留着自己投递用，网站不提供下载）；提交并推送。
它还会顺带检查英文版结构有没有跟上中文版。

跑之前确认本机装了 Word。`python-docx` 如果缺，脚本会自己装进 `.venv`。简历要是超过一页，
脚本会提醒一句。

**改站点的门面文字（首页介绍、方向、近况、作品、导航、按钮文案）** —— 改 `site_data.py`，
里面中英并列，改完 commit、push。

**改英文的简历内容** —— 改 `resume_data_en.py`。它的结构和中文版一一对应，
`python tools/check_i18n.py` 能检查有没有漏改。

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
streamlit_app.py          入口：建导航（页面清单来自 site_data.NAV），部署时主文件填这个
ui.py                     共用件：语言切换、主题样式、小节标题、侧边栏、页脚
site_data.py              站点文案：首页、作品、导航、界面文字、外链，中英并列（作品条目可带 link 外链）
resume_data.py            中文简历内容（由 publish.ps1 从 Word 同步，别手改）
resume_data_en.py         英文简历内容（手工维护，结构要和上面一致）
views/                    五个页面，一个文件一页
tools/publish.ps1         一键同步：文案 + PDF + 中英检查 + 提交推送
tools/sync_from_docx.py   从 Word 提取文案（被 publish.ps1 调用）
tools/check_i18n.py       检查中英两份简历内容结构是否一致
assets/avatar.jpg         证件照
assets/高宏曜-简历.pdf      由 publish.ps1 生成，留着自己投递用；网站不提供下载
.streamlit/config.toml    主题色，必须放仓库根目录，否则云端不读
.devcontainer/            Dev Container / Codespaces 配置
requirements.txt          锁了 streamlit==1.65.0，和本地验证过的版本一致
```

## 重新部署

share.streamlit.io → Create app → 选 "Yup, I have an app" → 点 "Paste GitHub URL"，粘
`https://github.com/Pseudosalieri/resume/blob/main/streamlit_app.py`，仓库、分支、主文件
三项会自动填好。App URL 那栏填一个记得住的子域名（目前在用的是 `gaohongyao-homepage`），
不填会生成一长串很难记的子域名；注意改过子域名之后旧地址会变成 404。

Advanced settings 里的 Python 版本选 3.12。这个选了之后不能再改，要换只能把应用删掉重新部署。

部署流程本身是照 [这篇](https://vocus.cc/article/69af99cefd89780001bfb6f0) 走的。

## 许可

代码按 [PolyForm Noncommercial License 1.0.0](LICENSE) 授权：非商业用途可以自由使用、
修改、分发，**商业用途不允许**。证件照、简历 PDF 和简历文案另算，见 [NOTICE.md](NOTICE.md)，
那部分连非商业转载也不允许。

## 踩过的坑

分页用的是 `st.navigation` + `st.Page`。一旦这么写，Streamlit 就不再看 `pages/` 目录那套
自动发现，页面必须在代码里显式登记；另外 `url_path` 只能是一段、不能带斜杠，所以语言没放进
路径，用的是 `?lang=en`。

免费版应用 12 小时没人访问就休眠，访客得点一下按钮唤醒。想让它一直醒着，可以拿 UptimeRobot
这类免费监控每隔几分钟 ping 一次。

网络这两条是踩过的：

本机已经配好全局代理（`git config --global http.proxy http://127.0.0.1:7897`），推拉都走它。
如果哪天把代理软件关了，git 会连不上，两种处理：临时绕过用 `git -c http.proxy= push origin main`；
彻底取消用 `git config --global --unset http.proxy`。`tools/publish.ps1` 的推送会依次尝试
当前配置 → 系统代理 → 完全不挂代理，三条都不行才报错并提示"提交已在本地"。

国内镜像解决不了推送：kkgithub 这类站点是只读缓存，不接受写入（而且实测它的证书已经对不上，
直接报 SNI/cert 错误）；gitclone.com 实测可以读（`git ls-remote
https://gitclone.com/github.com/Pseudosalieri/resume.git`）。要克隆大仓库时可以用它加速，
推送还是得靠上面的直连或代理。

应用默认是公开的，每周还会被搜索引擎抓一遍。页面上的手机号如果不想公开，把
`site_data.py` 里的 `SHOW_PHONE` 改成 `False`。

图片这类路径按仓库根目录解析，并且只能用 `/`。入口文件就在根目录，所以
`Path(__file__).parent` 正好等于仓库根；以后要是挪目录，记得这一条。

仓库改名的话，`site_data.py` 里的 `LINKS["github"]` 和上面那条部署链接要一起改。
