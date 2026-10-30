# 安装工作室（每台机器或每个工作区装一次）

工作室是一个 Node + Python 的小工具包，放在本技能的 `kit/` 文件夹里。要把它复制到一个可写的工作区文件夹，因为技能目录可能是只读的（也不该把渲染产物放进技能目录），而工作室需要在旁边放 `node_modules`、项目和渲染产物。

## 1. 找到 kit
- kit 是本技能根目录（`SKILL.md` 所在的文件夹）下的 `kit/`，通常是 `~/.claude/skills/kako-2d-studio/kit/`。注意区分：这是技能本身的文件夹；下面第 2 步在用户项目里建的工作室也叫 `kako-2d-studio/`。
- 路径不清楚时搜一下：`find / -path "*kako-2d-studio/kit/render.mjs" 2>/dev/null | head -1`（Linux / macOS / Cowork 虚拟机），或 `Get-ChildItem -Recurse -Filter render.mjs -Path $HOME\.claude | Select-Object -First 1`（PowerShell）。

## 2. 选工作区并复制
- 有用户连接的项目文件夹就用它，否则用当前工作目录。在里面建 `kako-2d-studio/`。
- `kako-2d-studio/` 已经存在且里面有 `render.mjs`，说明装过了。直接跳到第 5 步（环境检查），绝不覆盖用户的 `projects/` 文件夹。
- 把整个 `kit/` 复制进去：`cp -r "<kit>/." kako-2d-studio/`（bash）或 `Copy-Item -Recurse "<kit>\*" kako-2d-studio\`（PowerShell）。
- 在 `kako-2d-studio/` 里运行 `python3 tools/verify_kit.py`（这一步任何 Python 3 都行），必须报 29/29。有缺失或不一致的文件，就重新复制那几个。

## 3. 建 Python 虚拟环境
工作室的 Python 工具需要 Python ≥ 3.9。很多 Mac 自带或早年装的 `python3` 版本更老，Homebrew 和 Linux 的系统 Python 还可能禁止直接 `pip install`，所以一律在 `kako-2d-studio/` 里建一个专用虚拟环境：
1. 找一个 ≥ 3.9 的解释器：依次试 `python3 --version`、`python3.13`、`python3.12`、`python3.11`、`python3.10`（Windows：`py -3 --version`）。都没有时，装了 uv 就用 `uv python install 3.12`，否则按下表装 Python。
2. 在 `kako-2d-studio/` 里建环境：`<那个解释器> -m venv .venv`（或 `uv venv --python 3.12 .venv`）。已经有 `.venv` 就跳过。
3. **之后所有 `python ...` 命令都用这个环境里的 Python**：macOS / Linux 写 `.venv/bin/python`，Windows 写 `.venv\Scripts\python`。本技能文档里出现的 `python tools/...`、`python audio/...` 都按这个替换。

## 4. 安装依赖
用一个简短的列表告诉用户要装什么、为什么装：ffmpeg（视频 / 音频编码）、Node.js 依赖（渲染器、Three.js、字体，含中文的思源黑体 Noto Sans SC）、一个无头 Chromium（用来画每一帧）、numpy、scipy、faster-whisper 和 opencc（声音合成、对时、繁体转简体）。

| 需要 | Windows | macOS | Linux |
|---|---|---|---|
| ffmpeg + ffprobe | `winget install --id Gyan.FFmpeg -e`（装完开一个新终端） | `brew install ffmpeg` | `sudo apt-get install -y ffmpeg` |
| Node.js ≥ 18 | `winget install OpenJS.NodeJS.LTS` | `brew install node` | nodesource 或发行版自带的包 |
| Python ≥ 3.9 | python.org 安装包 | `brew install python` | 发行版自带的包 |
| JS 依赖 | `npm install`（在 kako-2d-studio 里） | 同左 | 同左 |
| 无头 Chromium | `npx playwright install chromium` | 同左 | 同左（缺库时 `npx playwright install-deps chromium`） |
| Python 依赖 | `.venv\Scripts\python -m pip install numpy scipy faster-whisper opencc-python-reimplemented` | `.venv/bin/python -m pip install …`（同左的包） | 同 macOS |

## 5. 检查和自测
1. `.venv/bin/python tools/doctor.py`（Windows：`.venv\Scripts\python tools\doctor.py`）。重复运行直到每一行都是 OK。加 `--install` 会自动执行 npm、playwright 和 pip 的修复命令，pip 会装进这个虚拟环境。
2. 自测：`node render.mjs --project examples/reaction-time --sheet --scale 0.3`。应该写出 `examples/reaction-time/build/sheets/sheet_01.png`，里面 14 张完成的画面（咖啡馆、大脸特写、一个 3D 环绕、蓝图图表、一张标题卡），并且不报错。打开 PNG 确认，然后删掉 `examples/reaction-time/build/`。（示例项目是英文的，只用来验证引擎能跑。）
3. Whisper 第一次运行时会下载模型（`base` 约 75 MB，`small` 约 500 MB，`large-v3` 约 3 GB），需要能访问 huggingface.co。

## 国内网络
先直接安装。下载失败或特别慢时，只在出问题的那一步换成国内镜像，不用改全局设置：
- npm 依赖：`npm install --registry=https://registry.npmmirror.com`
- 无头 Chromium：`PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright npx playwright install chromium`（Windows PowerShell 先运行 `$env:PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright"`）
- Python 依赖：pip 命令末尾加 `-i https://pypi.tuna.tsinghua.edu.cn/simple`
- Whisper 模型（从 huggingface.co 下载）：转写命令前面加 `HF_ENDPOINT=https://hf-mirror.com`（Windows PowerShell 先运行 `$env:HF_ENDPOINT="https://hf-mirror.com"`）

## 说明
- Linux 服务器和 Cowork 虚拟机没有 GPU。Chromium 会自动用 SwiftShader（Linux 默认 `--gl swiftshader`），都能跑，只是慢一些。
- Linux 上中文字体已经由 Noto Sans SC 包提供，不依赖系统字体；生僻字会回落到系统 CJK 字体（`sudo apt-get install -y fonts-noto-cjk`）。
- 磁盘：node_modules + Chromium 约 700 MB，再加渲染产物（10 分钟 1080p 的片子约 150–300 MB）。
- 更新：技能更新后（`git pull` 或换成新版文件夹），把新的 `kit/` 复制到已有的安装上（`cp -r "<kit>/." kako-2d-studio/`），不要动 `projects/`、`node_modules/` 和 `.venv/`，用户的片子是安全的。复制完运行 `tools/verify_kit.py` 应该报 29/29。加在 `engine/styles.js` 里的自定义配色需要重新加，覆盖前先检查。
