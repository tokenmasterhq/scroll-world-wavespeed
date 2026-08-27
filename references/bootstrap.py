#!/usr/bin/env python3
"""Bootstrap scroll-world-wavespeed's default WaveSpeed path.

No third-party Python packages are required. The script checks the default
toolchain, installs ffmpeg when a known package manager is available, writes the
local .env, and verifies the WaveSpeed key against the balance endpoint.
"""

from __future__ import annotations

import getpass
import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


WS_BASE = "https://api.wavespeed.ai/api/v3"
ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def has(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def install_ffmpeg() -> bool:
    if has("ffmpeg") and has("ffprobe"):
        return True

    system = platform.system().lower()
    candidates: list[list[str]] = []
    if system == "windows":
        if has("winget"):
            candidates.append(["winget", "install", "--id", "Gyan.FFmpeg", "-e", "--accept-package-agreements", "--accept-source-agreements"])
        if has("choco"):
            candidates.append(["choco", "install", "ffmpeg", "-y"])
        if has("scoop"):
            candidates.append(["scoop", "install", "ffmpeg"])
    elif system == "darwin":
        if has("brew"):
            candidates.append(["brew", "install", "ffmpeg"])
    else:
        if has("apt-get"):
            candidates.append(["sudo", "apt-get", "update"])
            candidates.append(["sudo", "apt-get", "install", "-y", "ffmpeg"])
        elif has("dnf"):
            candidates.append(["sudo", "dnf", "install", "-y", "ffmpeg"])
        elif has("pacman"):
            candidates.append(["sudo", "pacman", "-S", "--noconfirm", "ffmpeg"])
        elif has("apk"):
            candidates.append(["sudo", "apk", "add", "ffmpeg"])

    if not candidates:
        return False

    for cmd in candidates:
        print("+", " ".join(cmd))
        result = run(cmd)
        if result.returncode != 0:
            print(result.stderr.strip() or result.stdout.strip())
            if cmd[:2] == ["sudo", "apt-get"] and "update" in cmd:
                return False

    return has("ffmpeg") and has("ffprobe")


def read_env_key() -> str:
    if os.environ.get("WAVESPEED_API_KEY"):
        return os.environ["WAVESPEED_API_KEY"].strip()

    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith("WAVESPEED_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")

    return ""


def write_env_key(key: str) -> None:
    if not ENV_FILE.exists() and ENV_EXAMPLE.exists():
        ENV_FILE.write_text(ENV_EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")

    lines = ENV_FILE.read_text(encoding="utf-8").splitlines() if ENV_FILE.exists() else []
    wrote = False
    out: list[str] = []
    for line in lines:
        if line.startswith("WAVESPEED_API_KEY="):
            out.append(f"WAVESPEED_API_KEY={key}")
            wrote = True
        else:
            out.append(line)
    if not wrote:
        out.append(f"WAVESPEED_API_KEY={key}")
    ENV_FILE.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    try:
        ENV_FILE.chmod(ENV_FILE.stat().st_mode & ~(stat.S_IRWXG | stat.S_IRWXO))
    except OSError:
        pass


def check_key(key: str) -> tuple[bool, str]:
    req = urllib.request.Request(
        f"{WS_BASE}/balance",
        headers={"Authorization": f"Bearer {key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        balance = body.get("data", {}).get("balance")
        return True, f"WaveSpeed auth ok. Balance: {balance}"
    except urllib.error.HTTPError as exc:
        return False, f"WaveSpeed auth failed: HTTP {exc.code}"
    except Exception as exc:
        return False, f"WaveSpeed check failed: {exc}"


def main() -> int:
    print("scroll-world-wavespeed bootstrap: default WaveSpeed path")

    missing = [cmd for cmd in ("python3", "curl") if not has(cmd)]
    if "python3" in missing and has("python"):
        missing.remove("python3")
    if missing:
        print("Missing required command(s): " + ", ".join(missing))
        return 2

    if not install_ffmpeg():
        print("ffmpeg/ffprobe are required and could not be installed automatically.")
        print("Install ffmpeg with your OS package manager, then rerun this bootstrap.")
        return 3

    key = read_env_key()
    if not key or key == "your_wavespeed_api_key_here":
        if not sys.stdin.isatty():
            print("WAVESPEED_API_KEY is missing. Ask the user for it, then rerun:")
            print("  WAVESPEED_API_KEY=... python3 references/bootstrap.py")
            return 4
        key = getpass.getpass("Enter WAVESPEED_API_KEY (input hidden): ").strip()
        if not key:
            print("No key entered.")
            return 4

    ok, msg = check_key(key)
    print(msg)
    if not ok:
        return 5

    write_env_key(key)
    print(f"Wrote {ENV_FILE}")
    print("Ready: source .env before using references/pipeline.md WaveSpeed helpers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
