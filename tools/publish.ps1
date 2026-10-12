<#
  一键发布：把 Word 简历的最新内容同步到网站，并推送上线。

  做的事：
    1. 从 docx 逐字提取文案 → 重写 resume_data.py（并自动校验一致性）
    2. 从 docx 重新导出最新一页 PDF → assets/高宏曜-简历.pdf（这是网站唯一提供的下载件）
    3. git 提交并推送 → Streamlit Community Cloud 自动重新部署（约 1 分钟）

  用法：
    .\tools\publish.ps1                       # 同步 + 导出 PDF + 提交推送
    .\tools\publish.ps1 -NoPush               # 只同步与导出，不提交
    .\tools\publish.ps1 -Docx "D:\其它路径\简历.docx"
    .\tools\publish.ps1 -Message "更新科研经历"

  前置：本机装好 Microsoft Word（导出 PDF 用）。
#>
param(
    [string]$Docx = "",
    [string]$Message = "",
    [switch]$NoPush
)

$ErrorActionPreference = "Stop"
$tools = $PSScriptRoot
$root = Split-Path -Parent $tools            # website/
if (-not $Docx) { $Docx = Join-Path (Split-Path -Parent $root) "高宏曜 研发—理化分析开发方向.docx" }
if (-not (Test-Path -LiteralPath $Docx)) { throw "找不到简历 docx：$Docx" }
Write-Host ("源文件：{0}" -f $Docx)

# ---- 选择带 python-docx 的解释器（优先用仓库 venv）----
$py = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) { $py = "python" }
& $py -c "import docx" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "venv 内缺少 python-docx，正在安装…"
    & $py -m pip install -q python-docx
}

# ---- 1) 同步文案 ----
& $py (Join-Path $tools "sync_from_docx.py") $Docx
if ($LASTEXITCODE -ne 0) { throw "文案同步失败，已中止" }

# ---- 2) 重新导出 PDF（先复制到临时目录，绝不碰原 docx）----
$tmp = Join-Path $env:TEMP ("resume_publish_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tmp | Out-Null
$work = Join-Path $tmp "work.docx"
Copy-Item -LiteralPath $Docx $work -Force
$pdfOut = Join-Path $root "assets\高宏曜-简历.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false; $word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($work, $false, $true)
    $pages = $doc.ComputeStatistics(2)
    $doc.ExportAsFixedFormat($pdfOut, 17)
    $doc.Close($false)
} finally {
    $word.Quit(); [Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
}
Write-Host ("PDF 已更新（{0} 页）：{1}" -f $pages, $pdfOut)
if ($pages -ne 1) { Write-Warning "简历当前为 $pages 页，请确认是否要压缩到一页" }

# ---- 3) 提交并推送 ----
if ($NoPush) { Write-Host "已跳过提交（-NoPush）"; return }
Push-Location $root
try {
    git add -A
    if (git status --porcelain) {
        if (-not $Message) { $Message = "同步简历更新 " + (Get-Date -Format "yyyy-MM-dd HH:mm") }
        git commit -q -m $Message
        git push -q origin main
        Write-Host "已推送到 GitHub，社区云会在约 1 分钟内自动重新部署。"
    } else {
        Write-Host "内容没有变化，无需提交。"
    }
} finally { Pop-Location }
