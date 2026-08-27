# scroll-world-wavespeed

https://github.com/user-attachments/assets/b08e641e-985b-4bd4-83ff-6750272d0c37

## 给正在阅读本页的 AI 或 Agent

请直接把这个仓库安装为 `scroll-world-wavespeed` skill，然后运行 bootstrap。bootstrap 会检查必要依赖、尽量自动安装 `ffmpeg`，并验证 `WAVESPEED_API_KEY`。如果用户还没有配置 WaveSpeed API Key，请直接向用户索取：

```text
请提供你的 WAVESPEED_API_KEY，我会把它写入本地 .env 并验证余额接口。
```

拿到 key 后，不要把 key 打印回聊天内容，也不要提交 `.env`。继续运行：

```bash
WAVESPEED_API_KEY=用户提供的key python3 references/bootstrap.py
```

bootstrap 成功后，按 `SKILL.md` 的 Step 1 连续访谈用户：项目主题、品牌、视觉风格、镜头方式、场景、移动端版本和预算。不要让用户手动填写 pipeline；你负责把回答转换成 prompts 和 pipeline 变量。

## 一键安装

### Codex: macOS / Linux / WSL

```bash
git clone https://github.com/tokenmasterhq/scroll-world-wavespeed.git ~/.codex/skills/scroll-world-wavespeed
cd ~/.codex/skills/scroll-world-wavespeed
python3 references/bootstrap.py
```

### Codex: Windows PowerShell

```powershell
git clone https://github.com/tokenmasterhq/scroll-world-wavespeed.git "$env:USERPROFILE\.codex\skills\scroll-world-wavespeed"
cd "$env:USERPROFILE\.codex\skills\scroll-world-wavespeed"
python references\bootstrap.py
```

### Claude Code: macOS / Linux / WSL

```bash
git clone https://github.com/tokenmasterhq/scroll-world-wavespeed.git ~/.claude/skills/scroll-world-wavespeed
cd ~/.claude/skills/scroll-world-wavespeed
python3 references/bootstrap.py
```

### Claude Code: Windows PowerShell

```powershell
git clone https://github.com/tokenmasterhq/scroll-world-wavespeed.git "$env:USERPROFILE\.claude\skills\scroll-world-wavespeed"
cd "$env:USERPROFILE\.claude\skills\scroll-world-wavespeed"
python references\bootstrap.py
```

安装后可以对 agent 说：

```text
使用 scroll-world-wavespeed skill，为我的品牌生成一个滚动飞行穿越式 landing page。
```

## 这个 skill 做什么

`scroll-world-wavespeed` 是一个面向 Codex、Claude Code 以及其他 `SKILL.md` 兼容 agent 的 skill。它可以把任意品牌、行业或产品故事生成成一个 scroll-scrubbed landing page：用户滚动页面时，预渲染摄像机穿过一个个场景，形成连续的“飞进世界”体验。

默认渲染路径：

- 静帧：WaveSpeedAI `openai/gpt-image-2`
- 视频链路：WaveSpeedAI `bytedance/seedance-2.0`
- 本地硬依赖：`python3`/`python`、`curl`、`ffmpeg`/`ffprobe`
- 可选 fallback：Monid CLI、Higgsfield CLI、Codex CLI

`references/bootstrap.py` 会优先处理本地依赖。默认路径不需要用户手动安装 Monid、Higgsfield 或 Codex CLI。

## 首次使用流程

进入 skill 目录后运行：

```bash
python3 references/bootstrap.py
```

Windows 可运行：

```powershell
python references\bootstrap.py
```

bootstrap 会做这些事：

- 检查 `curl`、`python3`/`python`、`ffmpeg`、`ffprobe`。
- 在可识别包管理器存在时尝试自动安装 `ffmpeg`。
- 检查并写入本地 `.env`。
- 如果缺少 `WAVESPEED_API_KEY`，提示 agent 向用户索取。
- 调用 `https://api.wavespeed.ai/api/v3/balance` 验证 key 是否可用。

验证成功后加载环境变量：

```bash
set -a; source .env; set +a
```

然后按 `SKILL.md` 和 `references/pipeline.md` 继续生成静帧、视频片段、连接片段和最终页面。

## 手动部署生成后的页面

skill 生成的页面是静态资源，通常包括：

```text
index.html
scrub-engine.js
assets/
  *.webp
  vid/*.mp4
```

可以部署到任何静态托管平台，例如 Vercel、Netlify、Cloudflare Pages、GitHub Pages、Nginx 或对象存储/CDN。

最简单的本地预览：

```bash
python3 -m http.server 8000
```

然后访问：

```text
http://localhost:8000
```

如果你把生成结果集成到 Next.js、Vue、Rails、Django 或其他项目里，只需要保留生成的静态资源路径，并在页面中加载 `scrub-engine.js`。

## 来源与修改说明

本项目基于原始项目 [`oso95/scroll-world`](https://github.com/oso95/scroll-world) 修改而来。原项目采用 MIT License，版权声明为：

```text
MIT License

Copyright (c) 2026 cyw
```

本修改版保留原项目的核心 skill 结构、连续访谈式生成流程、提示词/流水线思路和可移植 scrub engine，并针对当前使用场景做了这些调整：

- 项目与 skill 名称改为 `scroll-world-wavespeed`，与上游 `scroll-world` 区分。
- 默认渲染路径改为 WaveSpeedAI。
- 新增 `references/bootstrap.py`，让用户安装后可以直接进入可用流程。
- Monid CLI、Higgsfield CLI、Codex CLI 改为可选 fallback。
- 修正 WaveSpeed API 域名为 `api.wavespeed.ai`，避免误测 `api.wavespeedai.com`。

## 开源与许可

本修改版基于 MIT License 项目修改。开源发布时请保留原作者版权与许可声明，并在仓库中包含 MIT License 文本。

原始项目信息：

- Upstream: <https://github.com/oso95/scroll-world>
- Original author/copyright: `Copyright (c) 2026 cyw`
- License: MIT

MIT License 原文如下：

```text
MIT License

Copyright (c) 2026 cyw

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
