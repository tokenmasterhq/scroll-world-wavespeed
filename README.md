<div align="center">

# 🌊 scroll-world-wavespeed

**滚动鼠标，镜头飞进你的品牌世界**

https://github.com/user-attachments/assets/b08e641e-985b-4bd4-83ff-6750272d0c37

一个给 AI 编程助手用的 skill —— 支持 Claude Code、Codex，以及任何兼容 `SKILL.md` 的 agent —— 能为任何行业或品牌生成一个沉浸式的「滚动飞行穿越世界」落地页：随着你往下滚，镜头从场景外一路飞进场景内部，再毫无剪辑地流向下一个场景。一整段连续不断的飞行，穿过一个生成出来的小世界（想象 Emons 物流官网那种效果，换成你想要的任何主题）。

在 [`oso95/scroll-world`](https://github.com/oso95/scroll-world) 原版的基础上，改用 WaveSpeedAI 重做并优化了整条使用流程。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Powered by WaveSpeedAI](https://img.shields.io/badge/powered%20by-WaveSpeedAI-6c5ce7)](https://wavespeed.ai)

</div>

---

## 🚀 三步开始（不用写代码）

1. 打开你的 AI 编程助手（Codex、Claude Code、WorkBuddy 等）
2. 把下面这段话原样复制粘贴过去
3. 跟着 AI 的提问回答就行：主题、品牌、风格、镜头、场景、要不要手机版、预算

```text
请打开并安装这个 skill：
https://github.com/enter-presser/scroll-world-wavespeed.git

按照 README 里的“给正在阅读本页的 AI 或 Agent”部分操作。
如果需要 WaveSpeed API Key，请直接问我要。
安装完成后，请连续询问我项目主题、品牌、视觉风格、
镜头方式、场景、是否需要移动端和预算，
然后帮我生成滚动飞行穿越式 landing page。
```

> 你不需要手动装依赖、改配置、写代码。AI agent 会处理这一切，只会在需要 WaveSpeed API Key 的时候问你要。

---

## ✨ 这个 skill 会做什么

把你的品牌 / 产品 / 行业故事，变成一个滚动式网页：鼠标往下滚，镜头像纪录片一样从一个场景飞进下一个场景，中间零剪辑衔接。

- 📱 可选生成手机端 9:16 竖屏版本
- 🖼️ 场景静帧与飞行视频均由 WaveSpeedAI 生成
- 🌐 生成结果是纯静态网页，随便找个地方（Vercel / Netlify / GitHub Pages）一放就能上线

<details>
<summary>💡 省钱建议</summary>
<br>

如果你只是想先看方向，请让 AI agent 先生成：

1. **Preview 版本**：用 `PREVIEW=1` 和 `VRES=480p` 生成低成本短视频链路。
2. **Final 版本**：确认满意后再生成 1080p 完整视频。

</details>

<details>
<summary>📦 生成出来的网页里有什么（给好奇的人看）</summary>
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

<details>
<summary>🤖 给正在阅读本页的 AI / Agent —— 点开看完整操作说明</summary>
<br>

你的目标：帮助没有代码经验的用户安装并使用 `scroll-world-wavespeed`。不要让用户手动填写 pipeline，不要让用户自己改 `.env`。

**请严格按下面的顺序执行 —— 顺序错了会卡住。**

1. **判断平台** —— 用户用的是 WorkBuddy、Claude Code、Codex，还是其他 `SKILL.md` 兼容 agent，据此在下面「安装命令」里选对应的那一条。

2. **安装** —— 执行该平台的 clone 命令。

3. **校验安装** —— 只认这一条命令的结果：

   ```bash
   test -f <安装目录>/SKILL.md && echo INSTALL_OK
   ```

   不要用 `ls` 判断成功与否。部分 agent 的沙箱看不见刚写入的工作树，`ls` 会返回空，让你误以为 clone 失败而反复重装。

4. **先向用户要 Key，再跑 bootstrap** —— 不要先裸跑 `references/bootstrap.py`。非交互环境下它缺 Key 会直接以 exit code 4 退出，你看到的现象会是「脚本跑了一行就结束」。先问用户：

   ```text
   请把你的 WaveSpeed API Key 发给我，我会自动写入本地配置并验证。
   ```

   （Key 在 <https://wavespeed.ai> 控制台获取。）

5. **带 Key 跑一次 bootstrap**

   macOS / Linux / WSL：

   ```bash
   cd <安装目录>
   WAVESPEED_API_KEY=用户提供的key python3 references/bootstrap.py
   ```

   Windows PowerShell：

   ```powershell
   cd <安装目录>
   $env:WAVESPEED_API_KEY="用户提供的key"
   python references\bootstrap.py
   ```

   看到 `WaveSpeed auth ok` 和 `Wrote ...\.env` 即为成功。不要把 Key 打印回聊天内容，不要提交 `.env`。

   > **ffmpeg 跨环境陷阱**：bootstrap 只能检测和安装**它自己所在环境**的 ffmpeg。在 Windows + WSL 上，如果你用 WSL 的 `python3` 跑 bootstrap，就必须用 WSL 的包管理器装（`sudo apt install -y ffmpeg`）—— 用 `winget` 装的 Windows 版 ffmpeg 在 WSL 里看不见，装了等于没装。全程保持在同一个环境里。

   > **余额**：bootstrap 会打印余额并在偏低时警告。参考量级：预览档一段 dive+connector 约 **$0.65**，成片档约 **$1.40**，N 个场景大约需要 N 段。余额不够一段就先让用户充值，不要开跑。

6. **连续访谈** —— bootstrap 成功后，按 `SKILL.md` 的 Step 1 访谈用户。**一次只问一个问题**，能用 `AskUserQuestion` 就用（给选项，别让用户对着空白自由发挥）。至少要问清楚：

   - 项目 / 品牌 / 产品主题
   - 品牌名、颜色、语气
   - 视觉风格
   - 镜头方式
   - 场景数量和场景内容
   - 是否需要移动端 9:16 版本
   - 预算或渲染档位

7. **开跑前确认** —— 把访谈结果汇总成一段人话，连同**预估总花费**（`N 张静帧 + (2N-1) 段视频`，要手机版则视频 ×2，再留 ~15% 重跑余量）一起发给用户，拿到明确的「开始」再生成。预算紧张时主动建议先跑 `PREVIEW=1 VRES=480p` 预览档，满意后再出成片。

</details>

<details>
<summary>📥 安装命令 —— 点开看各平台手动安装步骤</summary>
<br>

**WorkBuddy：macOS / Linux / WSL**

```bash
git clone https://github.com/enter-presser/scroll-world-wavespeed.git \
  ~/.workbuddy/skills/scroll-world-wavespeed
test -f ~/.workbuddy/skills/scroll-world-wavespeed/SKILL.md && echo INSTALL_OK
```

**WorkBuddy：Windows PowerShell**

```powershell
git clone https://github.com/enter-presser/scroll-world-wavespeed.git `
  "$env:USERPROFILE\.workbuddy\skills\scroll-world-wavespeed"
Test-Path "$env:USERPROFILE\.workbuddy\skills\scroll-world-wavespeed\SKILL.md"
```

**Claude Code：macOS / Linux / WSL**

```bash
git clone https://github.com/enter-presser/scroll-world-wavespeed.git \
  ~/.claude/skills/scroll-world-wavespeed
test -f ~/.claude/skills/scroll-world-wavespeed/SKILL.md && echo INSTALL_OK
```

**Claude Code：Windows PowerShell**

```powershell
git clone https://github.com/enter-presser/scroll-world-wavespeed.git `
  "$env:USERPROFILE\.claude\skills\scroll-world-wavespeed"
Test-Path "$env:USERPROFILE\.claude\skills\scroll-world-wavespeed\SKILL.md"
```

**Codex：macOS / Linux / WSL**

```bash
git clone https://github.com/enter-presser/scroll-world-wavespeed.git \
  ~/.codex/skills/scroll-world-wavespeed
test -f ~/.codex/skills/scroll-world-wavespeed/SKILL.md && echo INSTALL_OK
```

**Codex：Windows PowerShell**

```powershell
git clone https://github.com/enter-presser/scroll-world-wavespeed.git `
  "$env:USERPROFILE\.codex\skills\scroll-world-wavespeed"
Test-Path "$env:USERPROFILE\.codex\skills\scroll-world-wavespeed\SKILL.md"
```

装完不要在这里跑 bootstrap —— 回到上面「给正在阅读本页的 AI / Agent」的第 4、5 步，**先拿到 Key 再跑**。

</details>

<details>
<summary>📄 来源与许可</summary>
<br>

本项目基于 [`oso95/scroll-world`](https://github.com/oso95/scroll-world) 修改而来。原项目采用 MIT License。

原始版权声明：

```text
Copyright (c) 2026 cyw
```

本修改版保留原项目的核心 skill 结构、连续访谈式生成流程、提示词/流水线思路和可移植 scrub engine，并改为 WaveSpeedAI-first 路径。

开源发布时请保留 MIT License 和原作者版权声明，完整许可文本见 [LICENSE](LICENSE)。

</details>
