# AI漫剧 / AI comic open-source research (verified via gh CLI, 2026-10-20 UTC+8)
Stars/dates = live `gh` values at research time (last push date). Stars from gh search/repo view.

## Top finds
| # | Repo | Stars | Last push | What it does | Cost / requirements | Usefulness for us |
|---|---|---|---|---|---|---|
| 1 | [HBAI-Ltd/Toonflow-app](https://github.com/HBAI-Ltd/Toonflow-app) (MIT) | 18,503 | 2026-10-20 | 短剧/漫剧 platform: 剧本, 智能分镜, 角色/场景资产管理, image+video gen, infinite canvas, AI agent, MCP, local deploy | Free software; bring your own model APIs (README sponsors cite GPT-Image-2 ~$0.006/img via APIMart, MiniMax H3 video 0.09元/s) | ★★★★★ all-in-one GUI; use image path only, skip video |
| 2 | [ArcReel/ArcReel](https://github.com/ArcReel/ArcReel) (AGPL-3.0) | 5,600 | 2026-10-20 | Agent-driven self-hosted workspace: 小说/剧本 → 角色/场景/道具 assets → 分镜 → video → **剪映草稿 export**; cross-shot consistency; **cost tracking** | Self-host; paid text/image/video/TTS providers of your choice | ★★★★★ cost tracking + 剪映 export suits budget control |
| 3 | [eternityspring/shuohao-skills](https://github.com/eternityspring/shuohao-skills) (Apache-2.0) | 4,846 | 2026-10-15 | 7 agent skills: novel-outline, characters (bible+model sheets), character-refs, art bible (scene anchors), script, staging, storyboard | Runs in Claude Code/Codex etc.; only LLM + your image API | ★★★★★ best pre-production (story→script→分镜) |
| 4 | [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills) (MIT) | 3,089 | 2026-10-15 | 11 skills: 原著分析→分集剧本→视觉设定→分镜→image/video prompts→审查; "连续性锁" consistency phrases; preview-before-generate | Claude Code/Codex; vendor-neutral | ★★★★★ "confirm before production" = direct usage saving |
| 5 | [dramaclaw/dramaclaw](https://github.com/dramaclaw/dramaclaw) | 6,375 | 2026-10-20 | General AIGC video engine: script → finished film | Paid model APIs | ★★★ video-heavy; reference only |
| 6 | [shuyu-labs/BigBanana-AI-Director](https://github.com/shuyu-labs/BigBanana-AI-Director) | 2,354 | 2026-10-06 | AI 漫剧工场: Script→Asset→Keyframe workflow, character-consistency first, 配音, export | Software free (Docker/client); pay per API (AntSK API integration); README sells a paid course | ★★★★ good asset-first model; check license ("other") |
| 7 | [xuanyustudio/LocalMiniDrama](https://github.com/xuanyustudio/LocalMiniDrama) (MIT) | 2,150 | 2026-10-16 | Local (data stays on machine) short-drama/漫剧 tool; 通义/火山(豆包,Seedance 2.0)/可灵/Gemini/NanoBanana; workflow group re-run | Double-click app + your API keys; no GPU | ★★★★ easy start with 国内 APIs |
| 8 | [TypeTale/TypeTale](https://github.com/TypeTale/TypeTale) 字字动画 | 872 | 2026-08-21 | Free AIGC tool for AI短剧/小说推文: LLM extracts plot/characters, images via SD WebUI/ComfyUI/MJ/Nano Banana/Qwen, EdgeTTS/GPT-SoVITS/IndexTTS2, **剪映草稿 with auto keyframes (Ken Burns)** | Free; local GPU optional (ComfyUI) or API | ★★★★★ closest fit to "stills + light motion" 小说推文 style |
| 9 | [lhfer/codex-novel-to-comic-studio](https://github.com/lhfer/codex-novel-to-comic-studio) | 24 | 2026-10-17 | Codex SKILL.md: EPUB/TXT → story-first manga pages, PDF/CBZ | Codex + image API | ★★★ small but well-structured page/panel skill |
| 10 | [rany2/edge-tts](https://github.com/rany2/edge-tts) | 12,333 | 2026-10-14 | Free Microsoft Edge online TTS from Python, outputs subtitles (SRT/VTT) | Free, no GPU | ★★★★★ zero-cost narration + subs |
| 11 | [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice) (now QwenAudio/CosyVoice) | 24,064 | 2026-05-25 | Open multilingual TTS w/ zero-shot voice cloning | Local GPU recommended | ★★★★ distinct character voices for free if you have a GPU |
| 12 | [cubiq/ComfyUI_IPAdapter_plus](https://github.com/cubiq/ComfyUI_IPAdapter_plus) | 6,148 | 2025-04-14 | ComfyUI IP-Adapter nodes (face/style reference consistency) | Local GPU (~8GB+) | ★★★ only if going local SD/Flux; maintenance slowed |
Also seen: HVision-NKU/StoryDiffusion (6,484★, last push 2024-09, consistent self-attention – research, stale); YvonneMovingon/short-drama-skills (94★); xixihhhh/ai-short-drama-skill (60★); cosin2077/easyVoice (2,344★, multi-role TTS on edge-tts).
Note: `gh search` for ComfyUI consistency/PuLID returned mostly spam/empty; no strong standalone 系统流 prompt library found.

## Recommended low-cost pipeline (vertical 9:16, 系统流)
1. **Story/series bible** – shuohao-skills `novel-outline` or drama-skills 原著分析 in Claude Code/Codex (LLM tokens only). Define system UI rules (面板颜色, 提示音文案 "叮！") once.
2. **Episode script** – `novel-script` / drama-skills 分集剧本; 60–90s eps, 3s hook, cliffhanger, ~15–25 beats.
3. **分镜** – `novel-storyboard` / drama-skills storyboard → one JSON/CSV row per panel: shot size, characters, scene ID, dialogue, motion type (zoom-in/pan/shake).
4. **Consistent characters** – `character-refs` / `novel-characters`: one turnaround + expression sheet per character, plus a fixed "continuity lock" prompt phrase; feed as reference image to an image model that supports multi-image reference (Nano Banana/GPT-Image/Seedream via Toonflow/ArcReel/LocalMiniDrama), or IP-Adapter in ComfyUI if local GPU.
5. **Panels** – generate stills only (cheapest: ~cents/img API per README sponsor pricing). Toonflow or ArcReel asset library; batch per scene.
6. **Light motion + voice + subs** – TypeTale-style: edge-tts (free) or CosyVoice for voices with SRT; ffmpeg `zoompan` Ken Burns / 剪映 keyframes; system panels as overlay PNG/text animations in 剪映, not generated. Use real video gen (Seedance/H3) for ≤1–2 hero shots per episode max.
7. **Post** – ArcReel/TypeTale 剪映草稿 export → BGM, SFX ("叮"), 字幕 style template, cover; publish to 抖音/视频号.

## Usage-saving tricks
- Character reference sheets + continuity-lock text reused in every prompt → fewer rerolls.
- Background plates: generate each location once (empty, no people – shuohao `novel-art` "white plate"), composite/inpaint characters; reuse across episodes.
- Reuse expression bank (angry/smug/shocked) for close-ups; reuse system-UI overlay as a template, never generate it.
- Batch prompts per scene; draft at low res/cheap model, upscale only finals.
- Preview-then-confirm (drama-skills) and cost tracking (ArcReel) before any paid batch.
- Ken Burns/zoompan, parallax (split fg/bg), screen shake, flash cuts instead of video gen; 2–4s per panel.
- Free TTS (edge-tts) with auto subtitles; one 9:16 template for all eps.
