# scroll-world-wavespeed

https://github.com/user-attachments/assets/b08e641e-985b-4bd4-83ff-6750272d0c37

> 给 AI agent 的一句话：安装并使用 `scroll-world-wavespeed` skill，为用户连续追问项目主题、品牌、视觉风格、镜头、场景、移动端和预算，然后用 WaveSpeedAI 生成可滚动飞行穿越式 landing page。

`scroll-world-wavespeed` 是一个面向 Codex、Claude Code 以及其他 `SKILL.md` 兼容 agent 的 skill。它可以把任意品牌、行业或产品故事生成成一个 scroll-scrubbed landing page：用户滚动页面时，预渲染摄像机穿过一个个场景，形成连续的“飞进世界”体验。

## 来源与修改说明

本项目基于原始项目 [`oso95/scroll-world`](https://github.com/oso95/scroll-world) 修改而来。原项目采用 MIT License，版权声明为：

```text
MIT License

Copyright (c) 2026 cyw
```

本修改版保留原项目的核心 skill 结构、连续访谈式生成流程、提示词/流水线思路和可移植 scrub engine，并针对当前使用场景做了这些调整：

- 项目与 skill 名称改为 `scroll-world-wavespeed`，与上游 `scroll-world` 区分。
- 默认渲染路径改为 WaveSpeedAI：静帧使用 `openai/gpt-image-2`，视频链路使用 `bytedance/seedance-2.0`。
- 新增 `references/bootstrap.py`：首次使用时自动检查依赖、尽量自动安装 `ffmpeg`，并引导配置 `WAVESPEED_API_KEY`。
- Monid CLI、Higgsfield CLI、Codex CLI 改为可选 fallback，不再是默认路径的必装项。
- 修正 WaveSpeed API 域名为 `api.wavespeed.ai`，避免误测 `api.wavespeedai.com`。

## 安装给 AI Agent

### Codex

将本目录复制到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R scroll-world-wavespeed ~/.codex/skills/scroll-world-wavespeed
```

在 Codex 中可以直接说：

```text
使用 scroll-world-wavespeed skill，为我的品牌生成一个滚动飞行穿越式 landing page。
```

### Claude Code

将本目录复制到 Claude skills 目录：

```bash
mkdir -p ~/.claude/skills
cp -R scroll-world-wavespeed ~/.claude/skills/scroll-world-wavespeed
```

然后让 Claude Code 使用 `scroll-world-wavespeed` skill。

### 手动放入任意 SKILL.md 兼容环境

只要你的 agent 支持读取 `SKILL.md`，把整个目录作为一个 skill 放入对应 skills 目录即可：

```text
scroll-world-wavespeed/
├── SKILL.md
├── README.md
└── references/
    ├── bootstrap.py
    ├── pipeline.md
    ├── prompts.md
    ├── scrub-engine.js
    ├── index-template.html
    └── knockout.py
```

## 首次使用

进入 skill 目录后先运行 bootstrap：

```bash
python3 references/bootstrap.py
```

Windows 环境可使用：

```powershell
python references/bootstrap.py
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

## 配置项

默认路径只需要：

```bash
WAVESPEED_API_KEY=...
```

可选 fallback：

- Monid CLI：仅当用户明确选择 Monid/USD 计费路径时需要。
- Higgsfield CLI：仅当用户选择 Higgsfield credits 或需要 Higgsfield-only 模型时需要。
- Codex CLI：仅当希望用 Codex 的 image generation 能力生成静帧时才需要。

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
