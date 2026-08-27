# scroll-world-wavespeed

https://github.com/user-attachments/assets/b08e641e-985b-4bd4-83ff-6750272d0c37

一个给 AI 编程助手使用的 skill：通过连续提问，把你的品牌、产品或行业故事做成“滚动时镜头飞进世界”的网页。

## 如果你不是开发者

把下面这段话复制给你的 AI 编程助手（Codex、Claude Code、WorkBuddy 等）：

```text
请打开并安装这个 skill：
https://github.com/tokenmasterhq/scroll-world-wavespeed.git

按照 README 里的“给正在阅读本页的 AI 或 Agent”部分操作。
如果需要 WaveSpeed API Key，请直接问我要。
安装完成后，请连续询问我项目主题、品牌、视觉风格、镜头方式、场景、是否需要移动端和预算，然后帮我生成滚动飞行穿越式 landing page。
```

你不需要手动改代码。AI agent 会安装依赖、询问 API Key、配置环境，并一步步问你要生成网页需要的信息。

## 给正在阅读本页的 AI 或 Agent

你的目标：帮助没有代码经验的用户安装并使用 `scroll-world-wavespeed`。不要让用户手动填写 pipeline，不要让用户自己改 `.env`。

请按顺序执行：

1. 判断用户使用的是 Codex、Claude Code、WorkBuddy，还是其他 `SKILL.md` 兼容 agent。
2. 用下面的命令安装本 skill。
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

bootstrap 成功后，按 `SKILL.md` 的 Step 1 连续访谈用户，并把答案转换成 prompts 和 pipeline 变量。至少要问清楚：

- 项目/品牌/产品主题
- 品牌名、颜色、语气
- 视觉风格
- 镜头方式
- 场景数量和场景内容
- 是否需要移动端 9:16 版本
- 预算或渲染档位

## 安装命令

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

## 这个 skill 会做什么

`scroll-world-wavespeed` 会生成一个静态网页。页面通常包含：

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
- 必要本地工具：`python3`/`python`、`curl`、`ffmpeg`/`ffprobe`

`references/bootstrap.py` 会检查这些工具，并在可行时自动安装 `ffmpeg`。默认路径不需要用户手动安装 Monid、Higgsfield 或 Codex CLI。

生成后的网页可以部署到 Vercel、Netlify、Cloudflare Pages、GitHub Pages、Nginx 或任意静态托管服务。

本地预览：

```bash
python3 -m http.server 8000
```

然后访问：

```text
http://localhost:8000
```

## 来源与许可

本项目基于 [`oso95/scroll-world`](https://github.com/oso95/scroll-world) 修改而来。原项目采用 MIT License。

原始版权声明：

```text
Copyright (c) 2026 cyw
```

本修改版保留原项目的核心 skill 结构、连续访谈式生成流程、提示词/流水线思路和可移植 scrub engine，并改为 WaveSpeedAI-first 路径。

开源发布时请保留 MIT License 和原作者版权声明。
