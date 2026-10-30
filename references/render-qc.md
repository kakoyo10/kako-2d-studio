# 渲染、质检和排错

## 渲染

**先出预览。** `node render.mjs --project projects/my-video --from 0 --to 30 --scale 0.5` 写出 `build/preview.mp4`。看一遍（或抽几张静帧）。正式长渲之前，把预览或联系表发给用户。

**正式渲染：**
```bash
node render.mjs --project projects/my-video [--workers N] [--format jpeg]
python audio/mix.py --project projects/my-video        # 生成音乐 + 音效，混音，合成 -> out/<标题>.mp4
```
- worker 数默认是 CPU 线程数的一半（最多 8）。每个 worker 是一个独立的 Chromium。内存不够就少开（1080p 每个约 0.6–1.5 GB，4K 更多）。
- 没有 GPU 的机器（大多数 Linux 服务器）上，Chromium 用 SwiftShader（`--gl swiftshader`，Linux 默认）。Windows 和 macOS 桌面用 GPU（`--gl auto`）。
- **速度估算**（帧数 = 秒数 × 24）：在 2 线程云主机上渲 720p 约每秒 2 帧，47 秒的片子约 10 分钟。1080p 约 2 倍时间，1440p 约 3.5 倍，4K 约 8 倍。现在的 8 核台式机快 3–5 倍，GPU 对 3D 镜头帮助最大。按这个预估时间；10 分钟的 4K 片子要准备渲很久或者放一晚上。长渲放后台（`nohup … &` 或另开一个终端），隔一段时间看日志。
- `--format jpeg` 截图更快（约 1.5 倍），画质几乎没有损失。
- **修完局部重渲：** 整片重渲（简单稳妥），或者只渲改过的区间 `--from/--to --out build/fix.mp4`，再用 ffmpeg 拼回去（熟悉的话）。
- **成片质检：** `ffprobe` 时长 ≈ shots.json 时长、有音轨，再用 ffmpeg 给成片做一张联系表（`-vf fps=1/10,scale=320:-1,tile=6x5`）看一遍。

## 质检清单（每张联系表都过一遍）
- [ ] 没有 `MISSING SHOT` 或红色 `ERROR` 帧，终端没有打印镜头报错。
- [ ] 每张画面和它的 `line` 对得上，关键动作落在关键词上。
- [ ] 人物看得清：有轮廓光、站在亮的区域前、没有被画框切掉、没有压住文字。
- [ ] 同一场戏里服装和视线方向一致，每个人物都有接触阴影或站在地上。
- [ ] 暗调的明暗结构（大部分偏暗，1–3 个亮点），不灰不平，颜色来自 mood / style。
- [ ] 每个镜头都有运镜和一点氛围（灰尘 / 雨 / 粒子 / 光晕）。
- [ ] 文字短、在安全区内、手机上看得清。数字和旁白一致。中文没有方块（豆腐块）或明显的回落字体。
- [ ] 有变化：同一类型或景别的镜头连续不超过 3 个，中间穿插特写和插入镜头。
- [ ] 9:16：主体在中间，字幕下面没有重要内容。
- [ ] 声音：人声清楚、音乐已压低、音效不扎堆、总响度约 −14 LUFS。

## 排错
- **字体像默认的衬线字 / 中文是方块** → `@fontsource` 包没装好。在 kako-2d-studio 里运行 `npm install`；中文字体是 `@fontsource/noto-sans-sc`。
- **`Player failed to boot`** → 读报错信息。通常是 shots.json / config.json 的 JSON 语法错误，或者某个镜头的 import 路径错了。镜头的 import 错误会列在渲染结束时。
- **WebGL 或 3D 镜头全黑** → 加 `--gl swiftshader`，在终端里找 Three.js 报错（构建函数名拼错，或 init 里漏了 `return {stage}`）。
- **4K 内存不足或崩溃** → 用 `--workers 1` 或 `2`，4K 下别用太大的模糊（模糊的开销随分辨率增长）。
- **Whisper 模型下载失败** → 多半是连不上 huggingface.co，按 install.md「国内网络」加 `HF_ENDPOINT=https://hf-mirror.com` 重跑。**Whisper 慢** → 用 `--model base`。**脚本匹配率低（中文 < 85%，英文 < 90%）** → 脚本或配音不对，问用户。中文转写出现繁体字 → 确认装了 opencc，或者给 `--script` 让它按脚本原文对齐。
- **视频比音频长或短** → `story.duration` 必须等于最后一个镜头的 `end`。重跑 `beats.py --force` 或手动修。
- **faster-whisper 报 PyAV / `av` 错误** → 工具自己用 ffmpeg 解码音频，确认 ffmpeg 在 PATH 里就行。
- **Windows 路径** → 有空格的路径加引号。用 `python`（或 `py -3`）代替 `python3`。
