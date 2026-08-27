<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://api.iconify.design/tabler:aperture.svg?color=%23c9d1d9&height=34">
  <img src="https://api.iconify.design/tabler:aperture.svg?color=%2324292f&height=34" width="34" height="34" alt="">
</picture>

# scroll-world-wavespeed

**滚动鼠标，镜头飞进你的品牌世界**

https://github.com/user-attachments/assets/b08e641e-985b-4bd4-83ff-6750272d0c37

一个给 AI 编程助手用的 skill：连续问你几个问题，就能生成一个「滚动时镜头飞进场景」的落地页。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Powered by WaveSpeedAI](https://img.shields.io/badge/powered%20by-WaveSpeedAI-6c5ce7)](https://wavespeed.ai)

</div>

---

## <picture><source media="(prefers-color-scheme: dark)" srcset="https://api.iconify.design/tabler:rocket.svg?color=%23c9d1d9&height=22"><img src="https://api.iconify.design/tabler:rocket.svg?color=%2324292f&height=22" width="22" height="22" align="middle" alt=""></picture> 三步开始（不用写代码）

1. 打开你的 AI 编程助手（Codex、Claude Code、WorkBuddy 等）
2. 把下面这段话原样复制粘贴过去
3. 跟着 AI 的提问回答就行：主题、品牌、风格、镜头、场景、要不要手机版、预算

```text
请打开并安装这个 skill：
https://github.com/tokenmasterhq/scroll-world-wavespeed.git

按照 README 里的“给正在阅读本页的 AI 或 Agent”部分操作。
如果需要 WaveSpeed API Key，请直接问我要。
安装完成后，请连续询问我项目主题、品牌、视觉风格、镜头方式、场景、是否需要移动端和预算，然后帮我生成滚动飞行穿越式 landing page。
```

> 你不需要手动装依赖、改配置、写代码。AI agent 会处理这一切，只会在需要 WaveSpeed API Key 的时候问你要。

---

## <picture><source media="(prefers-color-scheme: dark)" srcset="https://api.iconify.design/tabler:sparkles.svg?color=%23c9d1d9&height=22"><img src="https://api.iconify.design/tabler:sparkles.svg?color=%2324292f&height=22" width="22" height="22" align="middle" alt=""></picture> 这个 skill 会做什么

把你的品牌 / 产品 / 行业故事，变成一个滚动式网页：鼠标往下滚，镜头像纪录片一样从一个场景飞进下一个场景，中间零剪辑衔接。

- 可选生成手机端 9:16 竖屏版本
- 场景静帧与飞行视频均由 WaveSpeedAI 生成
- 生成结果是纯静态网页，随便找个地方（Vercel / Netlify / GitHub Pages）一放就能上线

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://api.iconify.design/tabler:package.svg?color=%23c9d1d9&height=18"><img src="https://api.iconify.design/tabler:package.svg?color=%2324292f&height=18" width="18" height="18" align="middle" alt=""></picture> 生成出来的网页里有什么（给好奇的人看）</summary>
<br>

```text
index.html
scrub-engine.js
assets/
  *.webp
  vid/*.mp4
```

默认渲染路径：

- 静帧：WaveSpeedAI `openai/gpt-image-2`
- 视频：WaveSpeedAI `bytedance/seedance-2.0`
- 必要本地工具：`python3`/`python`、`curl`、`ffmpeg`/`ffprobe`（`references/bootstrap.py` 会自动检查，并在可行时自动装好 `ffmpeg`）

默认路径不需要手动安装 Monid、Higgsfield 或 Codex CLI。

本地预览：

```bash
python3 -m http.server 8000
```

然后访问 <http://localhost:8000>。

</details>

---

## <picture><source media="(prefers-color-scheme: dark)" srcset="https://api.iconify.design/tabler:bulb.svg?color=%23c9d1d9&height=22"><img src="https://api.iconify.design/tabler:bulb.svg?color=%2324292f&height=22" width="22" height="22" align="middle" alt=""></picture> 省钱建议

如果你只是想先看方向，请让 AI agent 先生成：

1. **静帧故事板**：只生成每个场景的 still image，不生成视频。
2. **Preview 版本**：用 `PREVIEW=1` 和 `VRES=480p` 生成低成本短视频链路。
3. **Final 版本**：确认满意后再生成 1080p 完整视频。

---

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://api.iconify.design/tabler:robot.svg?color=%23c9d1d9&height=18"><img src="https://api.iconify.design/tabler:robot.svg?color=%2324292f&height=18" width="18" height="18" align="middle" alt=""></picture> 给正在阅读本页的 AI / Agent —— 点开看完整操作说明</summary>
<br>

你的目标：帮助没有代码经验的用户安装并使用 `scroll-world-wavespeed`。不要让用户手动填写 pipeline，不要让用户自己改 `.env`。

请按顺序执行：

1. 判断用户使用的是 Codex、Claude Code、WorkBuddy，还是其他 `SKILL.md` 兼容 agent。
2. 用下面「安装命令」里对应平台的命令安装本 skill。
3. 运行 `references/bootstrap.py`。
4. 如果缺少 `WAVESPEED_API_KEY`，直接问用户：

   ```text
   请把你的 WaveSpeed API Key 发给我，我会自动写入本地配置并验证。
   ```

   拿到 key 后运行：

   ```bash
   WAVESPEED_API_KEY=用户提供的key python3 references/bootstrap.py
   ```

   Windows 可运行：

   ```powershell
   $env:WAVESPEED_API_KEY="用户提供的key"; python references\bootstrap.py
   ```

   不要把 key 打印回聊天内容，不要提交 `.env`。

5. bootstrap 成功后，按 `SKILL.md` 的 Step 1 连续访谈用户，并把答案转换成 prompts 和 pipeline 变量。至少要问清楚：
   - 项目 / 品牌 / 产品主题
   - 品牌名、颜色、语气
   - 视觉风格
   - 镜头方式
   - 场景数量和场景内容
   - 是否需要移动端 9:16 版本
   - 预算或渲染档位

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://api.iconify.design/tabler:download.svg?color=%23c9d1d9&height=18"><img src="https://api.iconify.design/tabler:download.svg?color=%2324292f&height=18" width="18" height="18" align="middle" alt=""></picture> 安装命令 —— 点开看各平台手动安装步骤</summary>
<br>

**Codex：macOS / Linux / WSL**

```bash
git clone https://github.com/tokenmasterhq/scroll-world-wavespeed.git ~/.codex/skills/scroll-world-wavespeed
cd ~/.codex/skills/scroll-world-wavespeed
python3 references/bootstrap.py
```

**Codex：Windows PowerShell**

```powershell
git clone https://github.com/tokenmasterhq/scroll-world-wavespeed.git "$env:USERPROFILE\.codex\skills\scroll-world-wavespeed"
cd "$env:USERPROFILE\.codex\skills\scroll-world-wavespeed"
python references\bootstrap.py
```

**Claude Code：macOS / Linux / WSL**

```bash
git clone https://github.com/tokenmasterhq/scroll-world-wavespeed.git ~/.claude/skills/scroll-world-wavespeed
cd ~/.claude/skills/scroll-world-wavespeed
python3 references/bootstrap.py
```

**Claude Code：Windows PowerShell**

```powershell
git clone https://github.com/tokenmasterhq/scroll-world-wavespeed.git "$env:USERPROFILE\.claude\skills\scroll-world-wavespeed"
cd "$env:USERPROFILE\.claude\skills\scroll-world-wavespeed"
python references\bootstrap.py
```

</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://api.iconify.design/tabler:file-text.svg?color=%23c9d1d9&height=18"><img src="https://api.iconify.design/tabler:file-text.svg?color=%2324292f&height=18" width="18" height="18" align="middle" alt=""></picture> 来源与许可</summary>
<br>

本项目基于 [`oso95/scroll-world`](https://github.com/oso95/scroll-world) 修改而来。原项目采用 MIT License。

原始版权声明：

```text
Copyright (c) 2026 cyw
```

本修改版保留原项目的核心 skill 结构、连续访谈式生成流程、提示词/流水线思路和可移植 scrub engine，并改为 WaveSpeedAI-first 路径。

开源发布时请保留 MIT License 和原作者版权声明，完整许可文本见 [LICENSE](LICENSE)。

</details>
