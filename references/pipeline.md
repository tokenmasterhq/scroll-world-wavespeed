# Pipeline: copy-paste scripts (bash 3.2 safe)

## 0. Bootstrap the default WaveSpeed path first

Run this once from the skill root before any generation:

```bash
python3 references/bootstrap.py   # or: python references/bootstrap.py on Windows
set -a; source .env; set +a
```

The bootstrap checks `curl`, `python3`/`python`, and `ffmpeg`/`ffprobe`, installs ffmpeg
when a known package manager is available, creates `.env`, and validates
`WAVESPEED_API_KEY` against `https://api.wavespeed.ai/api/v3/balance`. If it reports
that the key is missing, ask the user for `WAVESPEED_API_KEY` and rerun with:

```bash
WAVESPEED_API_KEY=... python3 references/bootstrap.py
```

Do not install or require Monid CLI, Higgsfield CLI, or Codex CLI for the default
WaveSpeed path. They are optional fallback paths only.

Set these once. `NAMES` is the ordered section ids; the last is the hero/finale.

```bash
WORK=/tmp/scroll-world-wavespeed # scratch dir for prompts, sources, frames
ASSETS=./assets                  # where the site reads stills (webp) + clips (mp4)
mkdir -p "$WORK" "$ASSETS/vid"
NAMES="farm kitchen shop delivery plaza finale"   # <-- your section ids, in order

# Chain video model 鈥?ONE for every chained clip (SKILL Step 4 roster).
# Must accept --start-image AND --end-image (verify: higgsfield model get <model>):
# seedance_2_0 | kling3_0 | seedance_2_0_mini (draft tier). Reference-only models can't
# hold a seam; models without --mode (e.g. kling3_0_turbo) need their own flag branch below.
# DEFAULT backend: WaveSpeedAI (section 7: gen_still_ws/gen_dive_ws/gen_conn_ws with
# VRES=1080p|720p|480p). The gen_dive/gen_conn functions in sections 2/4
# below are Higgsfield-credits fallbacks (and the only home of kling3_0/mini).
VMODEL=seedance_2_0
# Default backend is WaveSpeedAI. Use gen_still_ws/gen_dive_ws/gen_conn_ws in section 7.
# Monid, Higgsfield CLI, and Codex CLI snippets are optional fallbacks only.
case "$VMODEL" in                                  # per-model flags + durations (bash 3.2 safe)
  kling3_0)          VOPTS="--mode std --sound off";          DIVE_DUR=10; CONN_DUR=5 ;;  # no --resolution param on Kling
  seedance_2_0_mini) VOPTS="--mode std --resolution 720p";    DIVE_DUR=8;  CONN_DUR=5 ;;  # cheap frame-locked previz
  *)                 VOPTS="--mode std --resolution 1080p";   DIVE_DUR=8;  CONN_DUR=5 ;;  # seedance_2_0 default
esac

# Preview mode: PREVIEW=1 shortens every clip to 3s regardless of model 鈥?for
# validating style/motion/seam quality at the lowest possible spend BEFORE
# committing to the full-length batch above. Token-priced backends (WaveSpeed 搂7,
# Monid 搂7b) bill roughly linearly with duration, so 3s vs 8s cuts a dive's cost
# by more than half. Combine with VRES=480p (WaveSpeed) or a 2-scene NAMES subset
# (e.g. NAMES="farm kitchen") to get a full still鈫抎ive鈫抍onnector smoke test for
# a fraction of a full N-scene chain 鈥?e.g. observed WaveSpeed 480p pricing:
# ~$0.11/s of video, so a 3s preview dive+connector pair costs ~$0.65 total vs
# ~$1.40 at the default 8s/5s durations. Promote to PREVIEW=0 (or unset) and the
# full NAMES list only after the preview looks right 鈥?pacing/duration in the
# FINAL render should still follow the Step 4 camera-grammar table, not the
# preview shortcut.
PREVIEW="${PREVIEW:-0}"
if [ "$PREVIEW" = "1" ]; then DIVE_DUR=3; CONN_DUR=3; fi
```

Higgsfield generations take minutes 鈥?every `higgsfield ... --wait` call below is meant
to run inside a **backgrounded** script. Launch the whole script with your tool's
background/detached mode and poll the progress log; never block the foreground.

## 1. Scene stills (Step 2)

Write one prompt file per section to `$WORK/still_<name>.txt` (see prompts.md), then:

```bash
gen_still() { # name
  higgsfield generate create gpt_image_2 --prompt "$(cat "$WORK/still_$1.txt")" \
    --aspect_ratio 3:2 --resolution 2k --quality high --wait --wait-timeout 15m --json \
    > "$WORK/still_$1.json" 2> "$WORK/still_$1.err"
  url=$(jq -r '.[0].result_url // empty' "$WORK/still_$1.json")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/still_$1.png" && echo "still $1 ok" || echo "still $1 FAIL"
}
for n in $NAMES; do gen_still "$n" & done ; wait
```

Codex variant (STILLS_SOURCE=codex, SKILL Step 1.7 鈥?subscription-billed, zero
credits; ~1鈥? min each, parallelize in small batches):

```bash
gen_still_codex() { # name   (< /dev/null is REQUIRED for parallel calls 鈥?see SKILL Gotchas)
  codex exec -C "$WORK" -s workspace-write --skip-git-repo-check \
    'Use the image generation tool ($imagegen) to generate: '"$(cat "$WORK/still_$1.txt")"' Wide 3:2 landscape, high resolution. Save it as ./still_'"$1"'.png. Do not do anything else.' \
    > "$WORK/still_$1.codex.log" 2>&1 < /dev/null
  [ -f "$WORK/still_$1.png" ] && echo "still $1 ok (codex)" || echo "still $1 FAIL (see .codex.log)"
}
```

Convert to webp for the site (and optionally run knockout.py first for transparency):

```bash
for n in $NAMES; do cwebp -quiet -q 84 -resize 1800 0 "$WORK/still_$n.png" -o "$ASSETS/$n.webp"; done
```

Review the stills for cohesion before continuing. Re-roll any off-style one (optionally
add `--image "$WORK/still_<good>.png"` to lock style).

## 2. Dive-in clips (Step 4)

Prompt files at `$WORK/dive_<name>.txt`. Start image = the solid-bg still PNG.

```bash
gen_dive() { # name                       ($VOPTS is unquoted on purpose 鈥?word-split flags)
  higgsfield generate create "$VMODEL" --prompt "$(cat "$WORK/dive_$1.txt")" \
    --start-image "$WORK/still_$1.png" \
    $VOPTS --aspect_ratio 16:9 --duration "$DIVE_DUR" \
    --wait --wait-timeout 20m --json > "$WORK/dive_$1.json" 2> "$WORK/dive_$1.err"
  url=$(jq -r '.[0].result_url // empty' "$WORK/dive_$1.json")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/dive_$1.mp4" && echo "dive $1 ok" || echo "dive $1 FAIL"
}
for n in $NAMES; do gen_dive "$n" & done ; wait
```

Re-roll individual failures (503 / credit race are transient):
`gen_dive shop`  (just that one).

## 3. Extract boundary frames 鈥?the seam handoff (Step 5)

For each adjacent pair, the connector's start = dive_i's LAST frame, end = dive_{i+1}'s
FIRST frame 鈥?extracted from the **rendered videos**, never the stills.

```bash
set -- $NAMES
prev=""
for n in "$@"; do
  ffmpeg -v error -ss 0 -i "$WORK/dive_$n.mp4" -frames:v 1 -q:v 2 "$WORK/first_$n.png"      # establishing
  ffmpeg -v error -sseof -0.15 -i "$WORK/dive_$n.mp4" -frames:v 1 -q:v 2 "$WORK/last_$n.png" # interior
done
```

## 4. Connector clips (Step 5)

Prompt files at `$WORK/conn_<i>.txt` (i = 1..N-1). Iterate adjacent pairs:

```bash
gen_conn() { # i startPng endPng          (end-image required 鈫?seedance/kling3_0 only)
  higgsfield generate create "$VMODEL" --prompt "$(cat "$WORK/conn_$1.txt")" \
    --start-image "$2" --end-image "$3" \
    $VOPTS --aspect_ratio 16:9 --duration "$CONN_DUR" \
    --wait --wait-timeout 20m --json > "$WORK/conn_$1.json" 2> "$WORK/conn_$1.err"
  url=$(jq -r '.[0].result_url // empty' "$WORK/conn_$1.json")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/conn_$1.mp4" && echo "conn $1 ok" || echo "conn $1 FAIL"
}
set -- $NAMES ; i=0 ; prev=""
for n in "$@"; do
  if [ -n "$prev" ]; then i=$((i+1)); gen_conn "$i" "$WORK/last_$prev.png" "$WORK/first_$n.png" & fi
  prev="$n"
done ; wait
```

## 5. Encode everything for scrubbing (Step 6)

Native resolution (1080p from seedance std; kling3_0 std returned **720p** in testing 鈥?never upscale, encode what ffprobe reports), crf 20, GOP 8, light sharpen, no audio,
faststart. Same for dives + connectors.

```bash
enc() { ffmpeg -v error -y -i "$1" -an -vf "unsharp=5:5:0.8:5:5:0.0" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart "$2"; echo "enc $2 $(du -h "$2"|cut -f1)"; }

for n in $NAMES; do enc "$WORK/dive_$n.mp4" "$ASSETS/vid/$n.mp4"; done
i=0; for f in "$WORK"/conn_*.mp4; do i=$((i+1)); enc "$f" "$ASSETS/vid/conn$i.mp4"; done
```

Now the engine config's `sections[k].clip = assets/vid/<name>.mp4` and
`connectors = [assets/vid/conn1.mp4, 鈥` (length N-1, in order).

## 6. Centre-crop mobile encodes 鈥?FALLBACK ONLY, not the mobile version

**The mobile version is the native 9:16 portrait chain (搂6b).** This section's crop
encodes exist for one case: the user opted into mobile but credits can't cover the
portrait chain 鈥?and shipping them must be called out and approved, never silent
(portrait phones will see the landscape film's centre ~26%). The encode mechanics
matter either way: scrubbing sets `currentTime` every frame, and a phone decoder's
**seek cost scales with how many frames it must decode from the nearest keyframe** 鈥?so
a 1080p `-g 8` master that scrubs fine on a laptop stutters on a phone. A **smaller
frame + tighter GOP** fixes that (and halves the bytes on cellular). The crop `-m.mp4`
sibling per clip:

```bash
# 720p, GOP 4 (twice the keyframes = ~half the seek-decode work), crf 23, same sharpen/faststart.
encm() { ffmpeg -v error -y -i "$1" -an -vf "scale=-2:720,unsharp=5:5:0.6:5:5:0.0" \
  -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
  -g 4 -keyint_min 4 -sc_threshold 0 -movflags +faststart "$2"; echo "encm $2 $(du -h "$2"|cut -f1)"; }

for n in $NAMES; do encm "$WORK/dive_$n.mp4" "$ASSETS/vid/$n-m.mp4"; done
i=0; for f in "$WORK"/conn_*.mp4; do i=$((i+1)); encm "$f" "$ASSETS/vid/conn$i-m.mp4"; done
```

Wire the variants in the engine config 鈥?the engine serves them automatically on phones,
falling back to the desktop `clip` when a mobile one is absent:

```js
sections[k].clipMobile = 'assets/vid/<name>-m.mp4';
connectorsMobile = ['assets/vid/conn1-m.mp4', 鈥;   // length N-1, in order
```

If phone scrubbing still stutters, tighten the GOP further (`-g 2`, or `-g 1` for all-intra
= instant seeks at the cost of larger files); if cellular weight is the bigger worry, raise
`crf` (24鈥?6) or drop to `scale=-2:600`. If the master is already 720p (e.g. kling3_0 std),
the mobile encode still pays off 鈥?the tighter GOP is what makes phone seeks cheap. All-mobile encodes stay 16:9 鈥?the engine
centre-crops them; see the portrait note in SKILL Step 8 / prompts.md.

## 6b. Native 9:16 portrait chain 鈥?THE mobile version (Step 1.6 opt-in)

When the user opts into mobile, this is what they get: a **parallel 9:16 chain** rendered
natively for phones and shipped as the mobile variants 鈥?never the 搂6 crops (those are the
no-credits stopgap). Same seam laws as the main chain 鈥?the portrait chain frame-locks
against its own rendered frames, never the landscape ones. Budget ~2N-1 video gens +
re-rolls (interiors trip the NSFW filter in portrait too); state the credit cost at the
Step 1.6 interview.

1. **Portrait start canvases.** Don't hand the video model a 3:2 still and hope: composite
   each scene onto a 1080脳1920 canvas in the page bg colour (island at ~94% width, visual
   centre at ~45% height). The render then opens exactly on what the portrait poster shows.
   For knocked-out stills, composite the RGBA over the bg colour first.
2. **Dives/legs**: same prompt templates with a portrait clause up front ("Vertical
   portrait composition, the diorama centered with generous [bg] space above and below"),
   `--aspect_ratio 9:16`, same model/params as the main chain. Review each last frame
   before chaining, as ever.
3. **Connectors**: extract first/last frames **from the 9:16 renders** and generate 9:16
   connectors between them. A native 9:16 scene mixed into cropped-16:9 neighbours pops at
   both seams 鈥?the portrait chain must be complete, not partial.
4. **Encode** with the 搂6 settings but portrait-oriented scale: `scale=720:-2` (720 wide),
   `-g 4`, crf 23 鈫?these ARE the `-m.mp4` mobile files (and they replace any 搂6 crop
   stopgaps that shipped earlier).
5. **Posters**: extract each 9:16 dive's first frame 鈫?webp 鈫?wire as the section's
   `stillMobile` so the poster matches the portrait video's frame 0 (no landscape鈫抪ortrait
   flash when the clip paints). Engine support: `sections[k].stillMobile`.

## 7. WaveSpeed backend 鈥?Seedance 2.0, RMB pay-per-clip (the DEFAULT path; Higgsfield/Monid, 搂7b, are an alternate biller only, never required alongside this one)

WaveSpeedAI mirrors the same underlying model (`bytedance/seedance-2.0`) behind a
plain REST API, billed to card or **RMB via Alipay/WeChat** 鈥?use these functions in
the 搂2/搂4 loops. This is the primary, recommended path: it needs only `curl`,
`ffmpeg`/`ffprobe`, and `python3` (all near-universal) on top of a `WAVESPEED_API_KEY`
鈥?**no `jq`, no Higgsfield CLI, no Monid CLI, no OAuth login, no VPN.** `jq` is used
if present (faster) but every call below auto-falls-back to a bundled `python3`
extractor when `jq` is missing 鈥?do not hard-require `jq` when porting this section
into another runtime (e.g. a hosted agent sandbox that ships python3 but not jq).
Auth is a single bearer token:

```bash
# .env.example ships in the skill root 鈥?copy to .env (gitignored at the repo root),
# fill in the key, then: set -a; source .env; set +a
: "${WAVESPEED_API_KEY:?export WAVESPEED_API_KEY or source .env first}"
WS_BASE=https://api.wavespeed.ai/api/v3
WS_VIDEO_MODEL=bytedance/seedance-2.0        # image-to-video: image + optional last_image
WS_STILL_MODEL=openai/gpt-image-2            # text-to-image 鈥?same model Higgsfield used, confirmed schema

# jget FILE PATH 鈥?reads one field from a JSON response file. Uses jq if on $PATH,
# else falls back to a tiny python3 walker (dotted path, "foo.bar[0]" indexing).
# Every WaveSpeed helper below calls this instead of `jq -r` directly, so the whole
# backend runs with zero jq dependency.
if command -v jq >/dev/null 2>&1; then
  jget() { jq -r "$2 // empty" "$1" 2>/dev/null; }
else
  jget() { # file path
    python3 - "$1" "$2" <<'PY'
import json, sys
try:
    data = json.load(open(sys.argv[1]))
except Exception:
    print(""); sys.exit(0)
cur = data
for part in sys.argv[2].lstrip('.').split('.'):
    if not part:
        continue
    if '[' in part:
        key, idx = part[:-1].split('[')
        if key:
            cur = cur.get(key) if isinstance(cur, dict) else None
        if cur is None:
            break
        try:
            cur = cur[int(idx)]
        except Exception:
            cur = None
    else:
        cur = cur.get(part) if isinstance(cur, dict) else None
    if cur is None:
        break
print(cur if cur is not None else "")
PY
  }
fi

# jbody FILE key=value... 鈥?writes a flat JSON object to FILE without jq. Values that
# parse as a number/bool are typed accordingly; everything else is a string. Good
# enough for the flat WaveSpeed request bodies below (no jq -n dependency either).
jbody() { # outfile k=v ...
  out="$1"; shift
  python3 - "$out" "$@" <<'PY'
import json, sys
out = sys.argv[1]
body = {}
for kv in sys.argv[2:]:
    k, v = kv.split('=', 1)
    if v == 'true': body[k] = True
    elif v == 'false': body[k] = False
    elif v.lstrip('-').isdigit(): body[k] = int(v)
    else: body[k] = v
json.dump(body, open(out, 'w'))
PY
}
```

Same chain laws as everywhere else 鈥?only the I/O differs: uploads go through a
plain multipart endpoint (no signed-URL dance like Monid's `sfs`), the **confirmed**
request fields are **`image`** (start frame) and **`last_image`** (end frame,
optional 鈥?this is what turns a call into a connector instead of a leg), and runs
are fire-and-poll against the same `/predictions/{id}/result` shape your own test
script already used.

```bash
# helper: upload a local frame, print its public download URL (7-day expiry).
ws_upload() { # localPngOrJpg
  curl -fsS -X POST "$WS_BASE/media/upload/binary" \
    -H "Authorization: Bearer $WAVESPEED_API_KEY" \
    -F "file=@$1" -o /tmp/_ws_upload.json
  jget /tmp/_ws_upload.json ".data.download_url"
}

# fire-and-poll
ws_wait() { # predictionId outJson
  while :; do
    curl -fsS "$WS_BASE/predictions/$1/result" \
      -H "Authorization: Bearer $WAVESPEED_API_KEY" > "$2"
    case "$(jget "$2" ".data.status")" in
      completed|failed|cancelled|timeout|deleted) break ;;
    esac
    sleep 5
  done
}

gen_dive_ws() { # name   (VRES=480p|720p|1080p|4k; DIVE_DUR as usual)
  furl=$(ws_upload "$WORK/still_$1.png")
  jbody "$WORK/dive_$1.body.json" \
    prompt="$(cat "$WORK/dive_$1.txt")" image="$furl" aspect_ratio="16:9" \
    resolution="$VRES" duration="$DIVE_DUR" generate_audio=false enable_web_search=false
  rid=$(curl -fsS -X POST "$WS_BASE/$WS_VIDEO_MODEL/image-to-video" \
    -H "Authorization: Bearer $WAVESPEED_API_KEY" -H "Content-Type: application/json" \
    -d @"$WORK/dive_$1.body.json" -o /tmp/_ws_create.json; jget /tmp/_ws_create.json ".data.id")
  ws_wait "$rid" "$WORK/dive_$1.json"
  url=$(jget "$WORK/dive_$1.json" ".data.outputs[0]")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/dive_$1.mp4" && echo "dive $1 ok" \
    || echo "dive $1 FAIL ($(jget "$WORK/dive_$1.json" ".data.error")/$(jget "$WORK/dive_$1.json" ".data.status"))"
}

gen_conn_ws() { # i startPng endPng
  su=$(ws_upload "$2"); eu=$(ws_upload "$3")
  jbody "$WORK/conn_$1.body.json" \
    prompt="$(cat "$WORK/conn_$1.txt")" image="$su" last_image="$eu" aspect_ratio="16:9" \
    resolution="$VRES" duration="$CONN_DUR" generate_audio=false enable_web_search=false
  rid=$(curl -fsS -X POST "$WS_BASE/$WS_VIDEO_MODEL/image-to-video" \
    -H "Authorization: Bearer $WAVESPEED_API_KEY" -H "Content-Type: application/json" \
    -d @"$WORK/conn_$1.body.json" -o /tmp/_ws_create.json; jget /tmp/_ws_create.json ".data.id")
  ws_wait "$rid" "$WORK/conn_$1.json"
  url=$(jget "$WORK/conn_$1.json" ".data.outputs[0]")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/conn_$1.mp4" && echo "conn $1 ok" \
    || echo "conn $1 FAIL ($(jget "$WORK/conn_$1.json" ".data.error")/$(jget "$WORK/conn_$1.json" ".data.status"))"
}

# Stills 鈥?same model Higgsfield used (openai/gpt-image-2), confirmed schema.
gen_still_ws() { # name
  jbody "$WORK/still_$1.body.json" \
    prompt="$(cat "$WORK/still_$1.txt")" aspect_ratio="3:2" resolution="2k" quality="high"
  rid=$(curl -fsS -X POST "$WS_BASE/$WS_STILL_MODEL/text-to-image" \
    -H "Authorization: Bearer $WAVESPEED_API_KEY" -H "Content-Type: application/json" \
    -d @"$WORK/still_$1.body.json" -o /tmp/_ws_create.json; jget /tmp/_ws_create.json ".data.id")
  ws_wait "$rid" "$WORK/still_$1.json"
  url=$(jget "$WORK/still_$1.json" ".data.outputs[0]")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/still_$1.png" && echo "still $1 ok" \
    || echo "still $1 FAIL ($(jget "$WORK/still_$1.json" ".data.error")/$(jget "$WORK/still_$1.json" ".data.status"))"
}
```

Default usage in 搂1/搂2/搂4: `gen_still_ws` in place of `gen_still`,
`gen_dive_ws`/`gen_conn_ws` in place of `gen_dive`/`gen_conn` (mobile chain:
`aspect_ratio:"9:16"` and the 搂6b portrait canvases). Previz: same functions with
`VRES=480p` (pair with `PREVIEW=1` above for the cheapest possible smoke test).
Downloaded files are on a 7-day-expiry CDN 鈥?the functions download immediately,
don't defer it. No balance/credits CLI is documented for WaveSpeed, but the account
balance is readable directly: `curl -s https://api.wavespeed.ai/api/v3/balance -H
"Authorization: Bearer $WAVESPEED_API_KEY"` 鈫?`{"data":{"balance":N}}` (USD). Check it
before and after the first still + first dive to read the real per-clip cost before
batching the rest 鈥?same spirit as the Higgsfield calibration step (SKILL Step 1.7).

**Qualification harness 鈥?run this before trusting the chain for real** (each probe
= one cheap 480p clip, the same protocol this skill has always used before adopting
a new backend): (1) prompt + `image` from a real still 鈫?downloaded video's frame 0
must match the still (eyeball + PSNR 鈮?30 dB); (2) add `last_image` from a
*different* still 鈫?the final frame must land on that composition (a Seedance-style
near-miss is fine, the engine's crossfade covers it). If either probe fails, fall
back to `kwaivgi/kling-v3.0-std/image-to-video` on the same platform 鈥?its confirmed
schema uses `image` + `end_image` (not `last_image`) and has no
`aspect_ratio`/`resolution` fields, so it needs its own request-body branch, not a
drop-in var swap.

## 7b. Monid backend 鈥?Seedance 2.0 pay-per-clip (USD-only fallback; qualified 2026-07-25)

`bytedance /v1/video/seedance-2.0` via Monid is the roster's `seedance_2_0` billed
per clip in USD (a 1080p N=6 chain 鈮?$27) 鈥?use these functions in the 搂2/搂4 loops
for a non-CN build where the user prefers Monid/Higgsfield credits over WaveSpeed.
Same chain laws as everywhere else 鈥?only the I/O differs: **frames ride Monid's
free `sfs` file
system** (inline base64 is rejected), **`ratio` must be explicit** (the adaptive
default follows the input image's aspect), and runs are fire-and-poll. Token-priced
`w脳h脳24脳sec/1024` at $7/1M (480p/720p), $7.7/1M (1080p) 鈥?measured: 1080p 鈮?$2.99
dive / $1.87 connector; 720p 鈮?$1.21 / $0.76; 480p previz 鈮?$0.28 / $0.35.

```bash
# helper: upload a local frame to sfs, print a signed public URL for it ($0).
# NB: /cat and /ls take the SAME relative path you gave /put 鈥?not the
# "home/..."-prefixed path /put echoes back (that one 404s).
monid_frame_url() { # localPng remoteName  (JPEG-compresses on the way up)
  jpg="$WORK/sfs_$2.jpg"
  ffmpeg -v error -y -i "$1" -vf "scale='min(1536,iw)':-2" -q:v 2 "$jpg"
  size=$(stat -f%z "$jpg")
  up=$(NO_COLOR=1 monid run -p sfs -e /put \
    -i "{\"path\":\"chain/$2.jpg\",\"sizeBytes\":$size,\"ttl\":\"1h\"}" -w 60 -j \
    | jq -r '.output.uploadUrl')
  curl -fsS -T "$jpg" "$up" > /dev/null
  NO_COLOR=1 monid run -p sfs -e /cat -i "{\"path\":\"chain/$2.jpg\",\"ttl\":\"1d\"}" \
    -w 60 -j | jq -r '.output.url'
}

# fire-and-poll (the CLI's -w caps at 120s and seedance can exceed it)
monid_wait() { # runId outJson
  while :; do
    NO_COLOR=1 monid runs get -r "$1" -j > "$2" 2>/dev/null
    case "$(jq -r '.status // empty' "$2")" in
      COMPLETED|FAILED|BLOCKED|STOPPED|TIME_OUT) break ;;
    esac
    sleep 8
  done
}

gen_dive_monid() { # name   (VRES=1080p|720p|480p; DIVE_DUR as usual)
  furl=$(monid_frame_url "$WORK/still_$1.png" "still_$1")
  jq -n --arg p "$(cat "$WORK/dive_$1.txt")" --arg u "$furl" --arg r "$VRES" \
    '{content:[{type:"text",text:$p},
               {type:"image_url",image_url:{url:$u},role:"first_frame"}],
      resolution:$r, duration:'"$DIVE_DUR"', ratio:"16:9", generate_audio:false}' \
    > "$WORK/dive_$1.body.json"
  rid=$(NO_COLOR=1 monid run -p bytedance -e /v1/video/seedance-2.0 \
    -f "$WORK/dive_$1.body.json" -j | jq -r '.runId')
  monid_wait "$rid" "$WORK/dive_$1.json"
  url=$(jq -r '.output.content.video_url // empty' "$WORK/dive_$1.json")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/dive_$1.mp4" \
    && echo "dive $1 ok (\$$(jq -r '.cost.value' "$WORK/dive_$1.json"))" \
    || echo "dive $1 FAIL ($(jq -r '.status' "$WORK/dive_$1.json"))"
}

gen_conn_monid() { # i startPng endPng
  su=$(monid_frame_url "$2" "conn$1_start"); eu=$(monid_frame_url "$3" "conn$1_end")
  jq -n --arg p "$(cat "$WORK/conn_$1.txt")" --arg s "$su" --arg e "$eu" --arg r "$VRES" \
    '{content:[{type:"text",text:$p},
               {type:"image_url",image_url:{url:$s},role:"first_frame"},
               {type:"image_url",image_url:{url:$e},role:"last_frame"}],
      resolution:$r, duration:'"$CONN_DUR"', ratio:"16:9", generate_audio:false}' \
    > "$WORK/conn_$1.body.json"
  rid=$(NO_COLOR=1 monid run -p bytedance -e /v1/video/seedance-2.0 \
    -f "$WORK/conn_$1.body.json" -j | jq -r '.runId')
  monid_wait "$rid" "$WORK/conn_$1.json"
  url=$(jq -r '.output.content.video_url // empty' "$WORK/conn_$1.json")
  [ -n "$url" ] && curl -fsSL "$url" -o "$WORK/conn_$1.mp4" \
    && echo "conn $1 ok (\$$(jq -r '.cost.value' "$WORK/conn_$1.json"))" \
    || echo "conn $1 FAIL ($(jq -r '.status' "$WORK/conn_$1.json"))"
}
```

Default usage in 搂2/搂4: same loops, `gen_dive_monid`/`gen_conn_monid` in place of
the Higgsfield `gen_dive`/`gen_conn` (mobile chain: `ratio:"9:16"` and the 搂6b
portrait canvases). Previz: same functions with `VRES=480p`.
Result URLs expire (~24鈥?8 h) 鈥?the functions download immediately. Read the billed
`cost.value` per clip (echoed in the ok-line) and `monid balance` between phases; a
`BLOCKED` status is a workspace budget/run cap 鈥?terminal, surface it to the user.
Frame extraction, encoding, QA: identical to the Higgsfield path.

**Qualification harness for future/changed endpoints** (each probe = one cheap 480p
clip): (1) prompt + first_frame from a real still 鈫?downloaded video's frame 0 must
match the still (eyeball + PSNR 鈮?30 dB) and `cost.value` must match the advertised
cell; (2) add a last_frame from a *different* still 鈫?the final frame must land on
that composition (Seedance-style near-miss ok 鈥?the crossfade covers it). Known
failure to watch for (it's why the harness exists): `minimax /v1/video_generation`
still silently drops the image when `prompt` is present 鈥?image-only output proves
nothing about steerability.

## Notes

- `.[0].result_url` is the field on the `--wait --json` job object. `.min_result_url` is
  a lower-res preview if you ever want it.
- **NSFW fallback across models**: if one clip keeps getting flagged on seedance after
  re-rolls + prompt scrubbing, regenerate just that clip on `kling3_0` with the SAME
  start/end frames: `VMODEL=kling3_0; VOPTS="--mode std --sound off"; gen_conn 3 鈥 鈥?  then restore your chain model. See SKILL Gotchas for the trade-off.
- **Previz on the cheap**: run the whole chain once with `VMODEL=seedance_2_0_mini`
  (frame-locking intact, ~720p) to validate the journey and seams before spending
  full-model credits 鈥?because it's still seamless, the previz translates directly to the
  final render. Don't reach for reference-only models here: without `--start/--end-image`
  they can't hold a seam, so their output can't be chained (Step 4 rule).
- If a whole batch stalls, check `higgsfield workspace list` for credits and
  `$WORK/*.err` for the reason.
- Concurrency: launching ~5鈥? gens at once is fine; much more can trigger transient
  credit/race errors 鈥?stagger or re-roll.

