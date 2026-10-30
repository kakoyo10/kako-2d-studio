# kako-2d-studio · 中文 2D 火柴人动画 Skill

给 Claude Code 一段配音，它会做出一整支电影感的火柴人动画：黑色火柴人带一圈轮廓光，在暗调场景里把旁白演出来；中间有整屏的大脸特写、「时间暂停」定格、会跳动的数字和图表、蓝图风格的原理图，还有低多边形 3D 镜头；背景音乐和音效也是自动生成的。

每一帧都是代码画出来的，全程不调用任何图片或视频生成模型，所以角色长相前后一致，画面上的字始终清晰。不需要任何 API key。

- 配音可以是**中文**或**英文**；和你交流用中文。
- 16:9 或 9:16，720p / 1080p / 1440p / 4K。
- 六种配色：电影黄昏、午夜蓝、黄金时刻、霓虹黑色、柔和绘本、Kako 深紫。

## 需要什么
- Claude Code（Claude 桌面版的 Code 标签，或终端里的 `claude`），Pro 或以上订阅。
- macOS、Windows 或 Linux，约 1 GB 空闲磁盘。
- ffmpeg、Node.js ≥ 18、Python ≥ 3.9。没装也没关系，第一次使用时 Claude 会检查，缺什么告诉你怎么装。

## 安装
把这个仓库放进 Claude Code 的 skills 文件夹，文件夹名要叫 `kako-2d-studio`。

macOS / Linux：
```bash
git clone https://github.com/kakoyo10/kako-2d-studio.git ~/.claude/skills/kako-2d-studio
```

Windows（PowerShell）：
```powershell
git clone https://github.com/kakoyo10/kako-2d-studio.git "$HOME\.claude\skills\kako-2d-studio"
```

没装 git：在 GitHub 页面点 **Code → Download ZIP**，解压后把文件夹改名为 `kako-2d-studio`，放进 `~/.claude/skills/`（Windows 是 `C:\Users\你的用户名\.claude\skills\`）。

装完重启 Claude。

## 使用
1. 新建一个文件夹，把配音（`voiceover.wav`）放进去；有逐字一致的脚本就存成 `script.txt` 一起放进去，时间会对得更准。
2. 在 Claude 桌面版的 Code 标签里打开这个文件夹（或在这个文件夹里运行 `claude`）。模型建议 Opus 5.5，思考强度 High 或 Extra High。
3. 输入：
```text
/kako-2d-studio 用文件夹里的配音 voiceover.wav 和脚本 script.txt 做一支 2D 动画。配音是中文。
```
4. 依次回答 Claude 的问题（画面比例、分辨率、声音），看配色对比图选一种，看 30 秒预览，确认后渲染整片。
5. 成片在这个文件夹的 `kako-2d-studio/projects/<名字>/out/` 里。

第一次使用会在这个视频文件夹里装一份工作室（也叫 `kako-2d-studio/`，含依赖约 1 GB；和 `~/.claude/skills/` 里的技能文件夹是两样东西），需要联网下载 npm 包、Chromium 和 Whisper 语音模型。国内网络下载失败时，见 `references/install.md` 的「国内网络」一节。

做完以后只想改一部分，直接说就行：「换个配色」「第 12 个镜头人物被切掉了」「音乐太响」「改成 9:16 重新渲染」。

## 更新
```bash
git -C ~/.claude/skills/kako-2d-studio pull
```
然后重启 Claude。已经做过片子的文件夹里还有一份旧的工作室代码，在那个文件夹里跟 Claude 说：「kako-2d-studio 技能更新了，按 install.md 的更新说明把新 kit 覆盖到 kako-2d-studio/，保留 projects/」。

## 卸载
删掉 `~/.claude/skills/kako-2d-studio` 文件夹。

## 其他 AI 编程工具
`SKILL.md` 用的是 Agent Skills 格式，支持这个格式的工具（比如 Codex）把整个文件夹放进它们的 skills 目录也能用。流程需要工具能执行终端命令、能看图片（检查渲染出来的画面），效果以 Claude Code 为准。

## 目录
- `SKILL.md`：完整流程（Claude 读这个）
- `references/`：画风规则、故事拆解、引擎 API、声音设计、渲染质检、安装说明
- `kit/`：工作室代码：渲染器、动画引擎、对时工具、声音合成，以及一个英文示例项目
