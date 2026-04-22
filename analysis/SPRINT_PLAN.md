# SPRINT_PLAN — ccplugin-telegram

Date: 2026-04-22
Based on: MASTER_ANALYSIS.md

## Sprint 1 — Make it standalone (Run 1)

Goal: Plugin installable and functional without reading claude-config source.

| # | Task | File(s) | Est |
|---|------|---------|-----|
| T1 | Create `tg_parse.py` — parse getUpdates JSON, output TSV | `tg_parse.py` | 30m |
| T2 | Create `tg_send.py` — send text + optional keyboard to Telegram API | `tg_send.py` | 20m |
| T3 | Create `tg_voice.py` — Whisper transcription (openai-whisper → whisper.cpp → apple) | `tg_voice.py` | 30m |
| T4 | Create `install.sh` — copies all files to `~/.claude/plugins/telegram-bridge/`, checks secrets | `install.sh` | 20m |
| T5 | Fix SCRIPT_DIR in `telegram-poll.sh` — use resolved install dir, not source dir | `telegram-poll.sh` | 10m |

## Sprint 2 — Voice + UX (Run 2)

Goal: Voice messages work; restart capability; metadata fixes.

| # | Task | File(s) | Est |
|---|------|---------|-----|
| T1 | Wire VOICE branch in `telegram-poll.sh` — call tg_voice.py → run_claude | `telegram-poll.sh` | 20m |
| T2 | Add `/restart` command — reloads PROJECT_DIR from env or re-forks | `telegram-poll.sh` | 15m |
| T3 | Fix plugin.json `repository` URL | `.claude-plugin/plugin.json` | 5m |
| T4 | Add CHANGELOG.md — v1.0.0 → v1.1.0 → v1.2.0 (this run) | `CHANGELOG.md` | 20m |
| T5 | Add `telegram-ask.sh` — wait for Telegram reply, echo it; for use in agentic flows | `telegram-ask.sh` | 30m |

## Sprint 3 — Hardening (Run 3)

Goal: Production-grade reliability for unattended use.

| # | Task | File(s) | Est |
|---|------|---------|-----|
| T1 | Auth guard — reject non-CHAT_ID senders silently (log warning) | `telegram-poll.sh` | 15m |
| T2 | Configurable timeout via `CLAUDE_TIMEOUT` env var (default 300) | `telegram-poll.sh` | 10m |
| T3 | Robust offset dir — `mkdir -p` with error handling at startup | `telegram-poll.sh` | 10m |
| T4 | Progress streaming — send "still working..." at 60s intervals | `telegram-poll.sh` | 25m |
| T5 | Polish README — standalone quickstart (5 steps, no claude-config dependency) | `README.md` | 30m |
