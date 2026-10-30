# 声音设计

`audio/mix.py` 按 `story/shots.json` 生成整条音轨。人声出现时把音乐压低 −9 dB、环境声压低 −5 dB，再把总响度归一到 −14 LUFS（YouTube 标准），或者 `config.loudness` 指定的值。

**音乐规划**（shots.json 里的 `"music"`）：首尾相接的段落，每段一个情绪和强度（0–1；越高越多脉冲、琶音和鼓）。情绪：`mystery, tension, action, wonder, hopeful, sad, triumph, playful, calm, dark, epic`。在故事转折处换段（标题卡、发现、危险、高潮、收尾、原理讲解），一般 30–90 秒一段。试听：`python audio/music.py --mood tension --dur 20 --out test.wav`。用用户自己的曲子：设 `config.music.file = "input/music.mp3"`（会循环或截断，结尾淡出）。用 `config.music.gainDb`（默认相对人声 −17）调音乐大小。自动生成的音乐是能用的氛围 / 电影感铺底；想要更好的效果，建议用户换成自己有授权的曲子。

**音效**（每个镜头 `"sfx": [{"at": 0.3, "name": "whoosh", "gain": -8}]`，`at` 是距镜头开头的秒数；可选 `dur`、`seed`、`pitch`；`name` 也可以是用户自己的 WAV/MP3 路径）。音效库（`python audio/sfx.py --list` 列出，`--demo build/sfx_demo` 全部试听）：
`whoosh, swish, impact, hit, riser, slowmo, freeze, tick, clock, heartbeat, pop, blip, counter, ding, shimmer, stinger, footstep, kick, whistle, carpass, phonebuzz, phonering, cheer, applause, murmur, rain, thunder, wind, roomtone, city, hum, powerup, glitch, flash, buzz`。
惯例：甩镜和快速动作配 `whoosh` / `swish`。图形出现配 `pop` / `blip`，数字跳动垫 `counter`。大揭晓前 1–2 秒放 `riser`，揭晓时接 `impact` / `stinger`。进慢动作用 `slowmo`，时间暂停用 `freeze`。领悟和能力出现用 `ding` / `shimmer`。接触用 `hit` / `kick` / `footstep`。音量：轻的界面音 −12 到 −16，普通 −6 到 −10，大场面 −3 到 −6。同一时刻最多叠两个，别盖住人声。

**环境声**（每个镜头 `"amb": {"name": "rain", "gain": -20}`；循环播放，首尾 0.4 秒淡入淡出）：`rain, wind, city, roomtone, murmur, hum`。大多数镜头都加上，让世界听起来是连续的，音量 −18 到 −28。
