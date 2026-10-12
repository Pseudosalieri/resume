# 高宏曜 · 个人简历网站

用 Streamlit 写的个人简历站点，部署在 **Streamlit Community Cloud**（免费），线上地址形如
`https://<app-name>.streamlit.app`。

架构（与 [Streamlit + GitHub 如何變成 Web App](https://vocus.cc/article/69af99cefd89780001bfb6f0) 描述一致）：
GitHub 只负责存放代码 → Community Cloud 负责 Clone、建 Python 环境、`pip install`、
`streamlit run` 并对外提供 Web 服务；**推送到 GitHub 后网站会自动重新部署**。

## 目录结构

```
streamlit_app.py         入口文件（部署时在「Main file path」填这个路径）
resume_data.py           简历文案的唯一来源（改内容就改这里）
tools/sync_from_docx.py  可选：从 Word 版简历同步文案到 resume_data.py（本地工具）
assets/avatar.jpg        证件照（360×504，由 1 寸照缩放而来）
assets/高宏曜-简历.pdf     简历原件（供下载）
assets/高宏曜-简历.docx    简历原件（供下载）
.streamlit/config.toml   主题色等配置（须位于仓库根目录才会被云端读取）
requirements.txt         依赖（只有 streamlit）
```

## 本地预览

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

浏览器打开 http://localhost:8501 。注意：**必须在仓库根目录执行**，因为云端的工作目录
就是仓库根目录，本地保持一致的运行方式才能复现同样的路径解析结果。

## 部署到 Streamlit Community Cloud

1. 打开 <https://share.streamlit.io>，注册/登录账号（邮箱验证码、Google 或 GitHub 任选）。
2. 工作区里点 **Connect GitHub account** → **Authorize streamlit**（公开仓库即可）。
3. 右上角 **Create app** → 选择 **"Yup, I have an app"**。
4. 点 **Paste GitHub URL**，粘贴：

   ```
   https://github.com/Pseudosalieri/resume/blob/main/streamlit_app.py
   ```

   仓库、分支、主文件路径会自动填好（也可手填：Repository `Pseudosalieri/resume`、
   Branch `main`、Main file path `streamlit_app.py`）。
5. **App URL** 填一个好记的子域名，例如 `gaohongyao-resume`（全局唯一，被占用就换名字）。
   不填的话会自动生成一长串 `pseudosalieri-resume-streamlit-app-….streamlit.app`。
6. **Advanced settings** → **Python version 选 3.12**。⚠️ 部署后**不能修改** Python 版本，
   要换只能删掉应用重新部署。
7. 点 **Deploy**，多数应用几分钟内上线。

### 两个容易踩的点

* **入口文件名不会被自动识别**：对话框里的建议列表「不总是完整」，所以要么用上面的
  *Paste GitHub URL*，要么手动输入 `streamlit_app.py`。
* **部署要求对仓库有 admin 权限**：仓库建在你自己的账号下，你天然是 owner = admin，
  无需额外操作。但若将来把仓库**转进 GitHub 组织**，社区云需要该组织的 owner 在 OAuth
  授权页的 *Organization access* 里点 **Grant**（非 owner 只能 Request 等审批），否则就只能 fork。

## 日常更新简历

**方式一（推荐，纯网页文案）：** 直接改 `resume_data.py`，然后

```powershell
git add -A; git commit -m "更新简历内容"; git push
```

推送后社区云会自动重新构建并上线新版本（改依赖时重建要几分钟）。

**方式二（从 Word 简历同步）：** 先改好 Word 简历 `../高宏曜 研发—理化分析开发方向.docx`，再执行

```powershell
pip install python-docx          # 仅本地需要
python tools/sync_from_docx.py
```

脚本会逐字提取文案重写 `resume_data.py`，并自动校验每条文案都能在 docx 原文中找到。

**换证件照：** 把新照片存成 `assets/avatar.jpg`（建议 360×504 或更大、3:4.2 竖版）后 push 即可。

## 需要知道的平台行为与注意点

* **休眠**：应用 12 小时无访问会休眠，访客需在页面上点一下按钮唤醒（唤醒耗时官方未说明）。
  简历站访问稀疏，这是免费版的固有代价；想避免可用 UptimeRobot 之类的免费监控定时 ping 保活。
* **公开可检索**：应用默认公开，且每周会被搜索引擎收录。页面含邮箱与手机号；
  不想展示手机号就把 `streamlit_app.py` 顶部的 `SHOW_PHONE` 改成 `False`，或从
  `resume_data.py` 的 `fields` 里删掉电话那一项。
* **免费额度**：CPU 0.078–2 核、内存 690 MB–2.7 GB、存储 50 GB；超出会被限流或停机。
  本站只有静态内容，远低于上限。
* **资源路径**：`st.image`/`st.pdf` 等按**仓库根目录**解析路径，且只能用 `/`；本仓库入口
  文件就在根目录，因此 `Path(__file__).parent` 与仓库根一致。修改目录结构时请留意。
* **为什么没有内嵌 PDF 预览**：Streamlit 1.65 的 `st.pdf` 需要可选组件 `streamlit-pdf`
  （`pip install "streamlit[pdf]"`），但实测 `streamlit-pdf 2.1.0` 与该版本 Streamlit 的
  组件机制不兼容，导入即抛 `StreamlitAPIException: ... must be declared in pyproject.toml
  with asset_dir`。因此本站只提供下载，保持零第三方依赖。若将来官方修复，把
  `requirements.txt` 改成 `streamlit[pdf]` 并在「简历原件」标签页恢复 `st.pdf(...)` 即可。
* **仓库名变更**：若把仓库改名或改用 `resume-site`，请同步更新 `streamlit_app.py` 里的
  `GITHUB_URL` 与本文档中的部署链接。
