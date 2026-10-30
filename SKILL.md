---
name: kako-2d-studio
description: >
  当用户想用一段配音做一支 2D 火柴人动画时使用（电影感火柴人 + 轮廓光、暗调 2.5D 场景、整屏大脸特写、
  时间暂停定格、数据图表、蓝图原理图、低多边形 3D 镜头），例如「用这段配音做一支 2D 动画」「把我的脚本做成动画」
  「做一支火柴人动画」「做一期 What If / 如果……会怎样」「把旁白做成动画科普」「整支片子都做了」，
  或英文的 "make a 2D video from this voiceover" / "animate my script"。它跑完整条流程：安装、Whisper 对时、
  故事拆解、选配色、写镜头、渲染、音乐、音效，最后出 16:9 或 9:16、720p 到 4K 的 MP4。支持中文配音和中文画面字。
  已有项目只想重做某一步时也用它，例如「换个配色」「重新对时」「修一下这几个镜头」「给我看联系表」「重新渲染 / 渲 4K / 改竖屏」
  「换背景音乐 / 音乐太响」「重新混音」。
metadata:
  version: "0.1.0"
  author: Kako
---

# Kako 2D Studio：完整流程

把一段配音（脚本可选）做成一支完整的 MP4：每一帧都用代码画（HTML canvas + Three.js），在无头 Chromium 里逐帧截图，再用 ffmpeg 编码。全程不用图片或视频生成模型，所以角色前后一致、画面字清晰。每支片子的画面都按脚本重新设计，只有画风固定。

**全程用中文和用户交流**：提问、选项、进度、总结都用中文；文件名、命令、代码标识符保持英文。

**本技能附带的资源（本技能的根目录下）：**
- `kit/`：测试过的工作室（渲染器、引擎、工具、音频、`examples/reaction-time` 参考项目）。安装到工作区的 `kako-2d-studio/`（见 `references/install.md`）。
- `references/install.md`：安装、依赖表、环境检查、自测。
- `references/style-bible.md`：**画风**（人物、场景、光、镜头、剪辑、图形、中文字、9:16 规则、禁忌）。设计任何镜头之前先通读。
- `references/story-breakdown.md`：怎么写 `story/bible.md` 和 `story/shots.json`，以及节奏规则。
- `references/engine-api.md`：场景 API、config 和 shots.json 的结构、three-kit 参考。
- `references/sound-design.md`：音乐规划、音效库、环境声、电平。
- `references/render-qc.md`：预览和成片渲染、速度估算、质检清单、排错。

从头跑到尾时按第 1–8 阶段走，每到一个阶段再读对应的参考文档。用户只想重做某一步时，看文末「只重做某一步」。

## 黄金规则
1. **旁白一个字都不改。** 不改写、不增删、不调换顺序。每个镜头都只表现它在屏幕上时正在念的那几句。
2. **画风不变，画面全新。** 场景、道具、角色、动作都从这份脚本里来。`examples/reaction-time` 只用来学 API。
3. **念什么画什么，具体、字面。** 抽象的句子用视觉比喻、原理图或大脸特写的反应来表现。
4. **先出草图、自己看、修好，再渲染。** 正式渲染之前，自己打开联系表和静帧（读 PNG）检查。渲染慢，看图快。
5. **三个用户确认点**：开始时的设置选项、看渲染样张选配色、正式渲染前的预览。用户不在时按默认值走，说明用了哪些默认值，然后继续。
6. **以文件为准。** 每支片子放在 `kako-2d-studio/projects/<slug>/`，所有时间都以 `story/shots.json` 为准。

## 第 1 阶段：收集信息
一次问完（有 AskUserQuestion 就用它），用户已经说过的不再问：
- **配音文件**（必填）。
- **配音语言**：中文（默认）/ 英文 / 其他。
- **脚本**：带时间码的（SRT / VTT / JSON / 带 `[mm:ss]` 的 TXT）、纯文本（最好：和配音逐字一致）、或者没有（直接转写）。
- **画面比例**：16:9 或 9:16。
- **分辨率**：720p / 1080p（推荐）/ 1440p / 2160p（4K）。说明分辨率越高渲染越久。
- **字幕**：9:16 默认开，16:9 默认关。
- **音乐**：自动生成、用户自己的文件、不要。**音效**：开或关。
- **标题**。

这一步先不问配色。默认值：16:9、1080p、24 fps、中文、自动生成音乐 + 音效、配色 `dusk`。

## 第 2 阶段：安装或检查工作室
按 `references/install.md` 操作：把 `kit/` 复制到工作区的 `kako-2d-studio/`（已存在就跳过），在里面建 Python ≥ 3.9 的虚拟环境 `.venv`，安装依赖，运行 `tools/verify_kit.py` 和 `tools/doctor.py`，再跑示例自测。用一个简短的列表告诉用户装了什么。
**从这里开始，本文件里所有 `python ...` 命令都用 `.venv/bin/python`（Windows：`.venv\Scripts\python`）。**

## 第 3 阶段：建项目 + 时间轴
在 `kako-2d-studio/` 里运行，`python` 指 `.venv` 里的 Python。
```bash
python tools/new_project.py --name <slug> --voice "<配音路径>" [--script "<脚本路径>"] --aspect 16:9 --resolution 1080p --lang zh --title "<标题>" [--captions]
```
- `<slug>` 用英文小写和连字符（如 `slow-heartbeat`），标题可以是中文。
- **`--lang` 必须和配音语言一致**：中文配音 `--lang zh`，英文配音 `--lang en`（下面的转写命令也一样）。传错语言，Whisper 会按错误的语言识别，时间轴全部作废。
- 带时间码的脚本：`python tools/parse_script.py --project projects/<slug> --script projects/<slug>/input/script.<ext>`
- 纯文本脚本：`python tools/transcribe.py --project projects/<slug> --script projects/<slug>/input/script.txt --lang zh --model small`。中文按字对齐，匹配率要 ≥ 85%（英文 ≥ 90%）；低于这个数，告诉用户脚本和配音对不上。
- 没有脚本：`python tools/transcribe.py --project projects/<slug> --lang zh --model small`（机器慢用 `base`，中文没有脚本时建议 `medium` 或 `large-v3`，准确率高很多）。

检查 `timeline/transcript.txt`（结尾应该接近配音时长；中文应该是简体），然后运行 `python tools/beats.py --project projects/<slug>`，得到节拍表和一份 `story/shots.json` 草稿。

## 第 4 阶段：故事拆解
读 `references/style-bible.md` 和 `references/story-breakdown.md`。写 `story/bible.md`（一句话梗概、角色表——每人一个标志色、场景表——情绪和主光、视觉母题、音乐规划）。写 `scenes/cast.js`。重写 `story/shots.json`：镜头首尾相接，在短语边界前 0.1–0.2 秒切，镜头时长中位数 2–3.5 秒，每到一个新场景先给一个交代镜头，每个镜头写一句具体的 `scene` 描述。给用户发一段 5–10 行的方案摘要，用户没有异议就继续。

## 第 5 阶段：选配色
先做出用得最多的 1–2 个场景，加 3 个有代表性的镜头（一个至少两个角色的全景、一个 `bigFace` 大脸特写、一个数据 / 蓝图或 3D 镜头）。然后渲染：
```bash
node render.mjs --project projects/<slug> --styles dusk,midnight,golden,neon,storybook,kako --at <t1>,<t2>,<t3> --scale 0.5
```
打开 `build/styles/style_grid.png` 看一遍，再发给用户，每种配色一句话：**dusk 电影黄昏**（紫褐阴影、琥珀主光、奶油色轮廓光）、**midnight 午夜蓝**（冷海军蓝、蓝白轮廓光、钠灯橙）、**golden 黄金时刻**（暖橙配青）、**neon 霓虹黑色**（深黑、品红和青）、**storybook 柔和绘本**（浅粉彩、低对比）、**kako Kako 深紫**（深紫阴影、蓝白轮廓光、金色数字）。按这个故事推荐一种，让用户选。把选择存进 `config.json` → `style`。要微调就在 `engine/styles.js` 的 `STYLES` 里加一个自定义条目（moods 覆盖 + `grade` 的 lift/gamma/gain、sat、contrast、vignette、grain、bloom），重渲那一行。

## 第 6 阶段：写每一个镜头
先读一遍 `references/engine-api.md` 和 `examples/reaction-time/scenes/` 里的示例。每批 8–12 个镜头：
1. 写 `scenes/sets/<场景>.js`（可复用，锚定 `GY = E.H * V(0.8, 0.68)` 和 `CX = E.W/2`，墙、地面、天空延伸到画框外）和 `scenes/shots/NN_<名字>.js`，为 shots.json 里的每个 id 写 `registerShot('<id>', {...})`。
2. 运行 `node render.mjs --project projects/<slug> --sheet --scale 0.5`。打开每一张 `build/sheets/sheet_XX.png`，对照 `references/render-qc.md` 的质检清单检查。修好所有 MISSING 镜头、渲染器打印的错误和构图问题。
3. 检查动作：`--stills t1,t2,t3`，或 `--from A --to B --scale 0.5`（写出 `build/preview.mp4`）。

画风圣经里的硬性要求：
- 每个被照亮的人物都有轮廓光。
- 颜色取自 `mood()` / `S()`。
- 每个镜头都有运镜。
- 有氛围（灰尘、雨、光晕）。
- 暗调的明暗结构。
- 图形和念到的词同步，用 `wordTime()`（中文直接写中文词，如 `wordTime('十倍', info.shot.start)`）。
- 和画面比例有关的数值都用 `V()`。
- 不用 `Math.random` / `Date.now`。
- 画面上的字和配音同一种语言：中文配音写中文（标题每行 ≤ 8 个字，标签 ≤ 6 个字）；英文配音写英文（标题全大写，标签 1–3 个词）。

## 第 7 阶段：声音
读 `references/sound-design.md`。填 `story/shots.json` → `music`（首尾相接的情绪段），给每个镜头加 `sfx` 音效和 `amb` 环境声。混音在正式渲染之后（第 8 阶段）做；也可以现在运行 `python audio/mix.py --project projects/<slug>` 先听 `build/mix.wav`。

## 第 8 阶段：渲染和交付
读 `references/render-qc.md`。
1. 预览：`node render.mjs --project projects/<slug> --from 0 --to 30 --scale 0.5`。正式长渲之前，把预览或联系表给用户看，问用户是直接渲染还是要改（角色设计、颜色、某个镜头的动作都可以说）。
2. 成片：`node render.mjs --project projects/<slug>`。长片放后台跑并查看日志。日志会打印 fps 和预计剩余时间，把估算告诉用户。
3. 运行 `python audio/mix.py --project projects/<slug>`：生成音乐和音效，人声出现时压低音乐，响度归一到 −14 LUFS，合成 `out/<标题>.mp4`。
4. 检查成片：时长对得上、有音轨、每 10 秒一帧的联系表看起来没问题。交付 MP4（发送文件），用一句话说清文件存在哪里，再用一句话说下一步可以怎么改。

## 默认做法和判断
- 拿不准画面时，选更字面、更有电影感的：情绪用特写，物件用插入镜头，原理用蓝图，大空间用 3D。
- 每分钟大约 15–25 个镜头。每支片子 1–3 次定格，大约每分钟一个 3D 镜头。
- 每个角色的服装颜色全片不变，同一场戏里的视线方向保持一致。
- 只有用户能接受拼接时，才只重渲修好的那一段；否则整片重渲。

## 只重做某一步
先确认是哪个项目（`kako-2d-studio/projects/` 下有好几个时问用户），再只做对应的那一段。`python` 一律指 `kako-2d-studio/.venv` 里的 Python。
- **重新对时 / 换了配音或脚本**：重跑第 3 阶段。`parse_script.py` 支持 SRT、VTT、JSON（`[{start,end,text}]`、`{segments}`、`{words}`），以及 TXT 里 `[00:12.5] 文字`、`00:12 - 00:15 文字`、`00:00:12,500 --> 00:00:15,000 文字` 这样的行；找不到时间码就改用 `transcribe.py --script`。`beats.py` 要覆盖已有的 shots.json 时加 `--force`，会丢掉已经写好的镜头描述，先问用户。
- **换配色**：对比图一定用用户自己的镜头。完成的镜头少于 3 个时，先按第 5 阶段做出代表镜头；每个镜头取约 45% 处的时刻。要自定义配色：在 `engine/styles.js` 的 `STYLES` 里复制最接近的预设、起新 id，调 `moods` 覆盖（`sky`、`key`、`rim`、`wall`、`floor`、`practical`）、`grade`（`lift` 染暗部、`gain` 染亮部、`gamma`、`sat`、`contrast`、`vignette`、`grain`、`bloom`）和 `ui` 颜色，用 `--styles <新id>,<最接近的预设>` 重渲给用户对比。之后 `verify_kit.py` 会报 `engine/styles.js` 有改动，这是正常的。某个镜头不跟着变色，就是里面有写死的颜色，换成 `mood()` / `S()`。
- **修镜头 / 看联系表**：`node render.mjs --project projects/<slug> --sheet --scale 0.4` 会列出 MISSING 镜头和报错；修完重出联系表，**打开每一张 PNG** 对照 `references/render-qc.md` 的质检清单。
- **重新渲染 / 改分辨率或比例**：改 `config.json` 的 `resolution` / `aspect`（换比例要重新看一遍联系表，9:16 构图不同）。超过一两分钟的渲染放后台：`nohup node render.mjs --project projects/<slug> > build/render.log 2>&1 &`，隔一段时间看日志，汇报进度和预计剩余时间。内存紧张就用 `--workers 1` 或 `2`（1080p 每个 worker 约 1–1.5 GB）；没有 GPU 加 `--gl swiftshader`。输出 `build/video_silent.mp4`，再跑 `audio/mix.py` 合成成片。
- **声音**：按 `references/sound-design.md` 改 `story/shots.json` 的 `music` 和各镜头的 `sfx` / `amb`。试听某种情绪：`python audio/music.py --mood tension --intensity 0.7 --dur 20 --out build/test_tension.wav`；列出音效：`python audio/sfx.py --list`。用户自己的曲子：复制到 `projects/<slug>/input/`，设 `config.json` → `"music": {"enabled": true, "file": "input/<文件名>.mp3", "gainDb": -17}`；不要音乐：`"music": {"enabled": false}`。音乐或音效太响太小，改 `config.music.gainDb` / `config.sfx.gainDb`，每次 2–3 dB。改完重跑 `python audio/mix.py --project projects/<slug>`，用 `ffmpeg -i out/<文件>.mp4 -af ebur128=framelog=quiet -f null -` 确认整体响度约 −14 LUFS。
