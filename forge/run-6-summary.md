# Forge Run 6 Summary — ccplugin-telegram

**Date:** 2026-04-22
**Runs:** 3 (Sprint 1–3)
**Commits:** 3

## Stats

- Files created: 6 (tg_parse.py, tg_send.py, tg_voice.py, install.sh, telegram-ask.sh, CHANGELOG.md)
- Files modified: 3 (telegram-poll.sh, README.md, plugin.json)
- Issues created: 3 (GitHub #1, #2, #3)

## Deliverables by Run

### Run 1 — Standalone install
- `tg_parse.py` — Telegram response parser, emits TSV (MSG/CB/PHOTO/DOC/VOICE)
- `tg_send.py` — Telegram sender, auto-splits >4096 char messages
- `tg_voice.py` — Multi-backend transcription: openai-whisper → whisper-cpp → apple → openai-api
- `install.sh` — One-command installer with secrets check
- Fixed SCRIPT_DIR to prefer installed location

### Run 2 — Voice + UX
- Wired VOICE branch: OGG download → tg_voice.py → run_claude
- Added `/restart [project]` — hot-restart without SSH
- `telegram-ask.sh` — wait-for-reply helper for agentic flows
- CHANGELOG.md added
- plugin.json repository URL fixed

### Run 3 — Hardening
- Progress streaming: typing indicator + "still working..." every 60s
- `CLAUDE_TIMEOUT` env var (default 300s, configurable)
- Robust `~/.watchdog` dir creation
- Empty output warning
- README: standalone 5-step quickstart

## Lessons

1. **Python helpers must live in the repo** — Any plugin that references external scripts is non-functional as a marketplace install. Check all `source_dir` vs `install_dir` references at creation time.
2. **Voice support was 90% there** — The download path + Claude routing was already written for PHOTO/DOC. Wire VOICE the same way; just add `tg_voice.py` and it works.
3. **Progress streaming is critical for trust** — 300s silent wait looks broken to users. A 60s heartbeat completely changes perceived reliability.
4. **Agentic helpers (telegram-ask.sh) unlock unattended workflows** — Without this, Claude can't ask questions when away.
